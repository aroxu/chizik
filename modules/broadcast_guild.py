import typing
import aiohttp
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from db.index import DB
from models.guild import Guild
from views.stream_alert import StreamAlertCreateConfirm
from views.stream_alert_info import StreamAlertInfo

BASE_URL = "https://api.chzzk.naver.com/service/v1/channels/"


class BroadcastGuildAlert(commands.GroupCog, name="방송알림"):
    def __init__(self, bot: commands.Bot, session: aiohttp.ClientSession) -> None:
        self.bot = bot
        self.session = session
        self.alert_job.start()

    async def cog_unload(self) -> None:
        self.alert_job.cancel()
        return await super().cog_unload()

    async def fetch_streamer_info(self, channel_id: str):
        try:
            async with self.session.get(f"{BASE_URL}{channel_id}") as streamer_info:
                streamer_info.raise_for_status()
                return await streamer_info.json()
        except aiohttp.ClientResponseError as e:
            # Handle specific HTTP response errors
            print(f"Error fetching streamer info: {e}")
            return None
        except Exception as e:
            # Handle other exceptions
            print(f"Unexpected error fetching streamer info: {e}")
            return None

    async def fetch_stream_info(self, channel_id: str):
        try:
            async with self.session.get(f"{BASE_URL}{channel_id}/live-detail") as streamer_info:
                streamer_info.raise_for_status()
                return await streamer_info.json()
        except aiohttp.ClientResponseError as e:
            # Handle specific HTTP response errors
            print(f"Error fetching streamer info: {e}")
            return None
        except Exception as e:
            # Handle other exceptions
            print(f"Unexpected error fetching streamer info: {e}")
            return None

    @tasks.loop(minutes=3)
    async def alert_job(self):
        try:
            with DB().getSession() as session:
                statements = session.query(
                    Guild).filter_by(activated=True).all()
                for statement in statements:
                    streamer_info = await self.fetch_streamer_info(statement.streamer_id)
                    streamer_info = streamer_info["content"]

                    if streamer_info["channelId"] is None:
                        continue

                    stream_info_data = await self.fetch_stream_info(statement.streamer_id)
                    stream_info_data = stream_info_data["content"]

                    if streamer_info["openLive"]:
                        if statement.is_streaming == True:
                            continue
                        else:
                            statement.is_streaming = True
                            session.commit()
                            embed = discord.Embed(
                                title=streamer_info["channelName"], description=streamer_info["channelDescription"], color=0x00ff00)
                            embed.url = f"https://chzzk.naver.com/{statement.streamer_id}"
                            embed.set_footer(text=statement.streamer_id)
                            embed.timestamp = discord.utils.utcnow()
                            embed.set_image(
                                url=stream_info_data["liveImageUrl"].replace("{type}", "720"))
                            embed.set_thumbnail(
                                url=streamer_info["channelImageUrl"])
                            embed.add_field(
                                name="시청자 수", value=f"{stream_info_data['concurrentUserCount']}명")
                            embed.add_field(
                                name="카테고리", value=f"{'미정' if stream_info_data['liveCategoryValue'] == '' else stream_info_data['liveCategoryValue']}")
                            channel = await self.bot.fetch_channel(statement.alert_channel)
                            await channel.send(content=statement.alert_text, embed=embed, allowed_mentions=discord.AllowedMentions(everyone=True))
                            continue
                    else:
                        if statement.is_streaming == False:
                            continue
                        else:
                            statement.is_streaming = False
                            session.commit()
                            continue
        except Exception as e:
            print(e)
            pass

    @app_commands.guild_only()
    @app_commands.command(name="설정", description="방송 알림을 설정합니다.")
    @app_commands.describe(channel_id="스트리머의 채널 ID", alert_channel="알림을 받을 채널", alert_text="알림과 함께 전송될 메세지")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def _set_stream_alert(self, interaction: discord.Interaction,
                                channel_id: str, alert_channel: typing.Union[discord.TextChannel, discord.Thread],
                                alert_text: typing.Optional[str]) -> None:
        streamer_info = await self.fetch_streamer_info(channel_id)

        if not streamer_info or streamer_info["code"] != 200:
            await interaction.response.send_message("채널을 찾을 수 없습니다.")
            return

        streamer_info = streamer_info["content"]
        if streamer_info["channelId"] is None:
            await interaction.response.send_message("채널을 찾을 수 없습니다.")
            return

        stream_info_data = await self.fetch_stream_info(channel_id)
        if not stream_info_data or stream_info_data["code"] != 200:
            await interaction.response.send_message("치지직 서버 오류입니다.")
            return
        if stream_info_data["content"] == None:
            await interaction.response.send_message("해당 채널은 방송 채널이 아닌 것 같습니다. 방송이 가능한 사용자인지 확인해주세요.")
            return

        stream_info_data = stream_info_data["content"]

        embed = discord.Embed(
            title=streamer_info["channelName"], description=streamer_info["channelDescription"], color=0x00ff00)
        embed.url = f"https://chzzk.naver.com/{channel_id}"
        embed.set_footer(text=channel_id)
        embed.timestamp = discord.utils.utcnow()
        embed.set_image(
            url=stream_info_data["liveImageUrl"].replace("{type}", "720"))
        embed.set_thumbnail(url=streamer_info["channelImageUrl"])
        embed.add_field(
            name="시청자 수", value=f"{stream_info_data['concurrentUserCount']}명")
        embed.add_field(
            name="카테고리", value=f"{'미정' if stream_info_data['liveCategoryValue'] == '' else stream_info_data['liveCategoryValue']}")

        view = StreamAlertCreateConfirm(timeout=15, interaction=interaction,
                                        channel_id=channel_id, alert_channel=alert_channel, alert_text=alert_text)

        await interaction.response.send_message(content=f"방송 시작이 감지되면 아래와 같이 메세지가 발송됩니다.\n\n{alert_text if alert_text else ''}", embed=embed, view=view, delete_after=15)

    @app_commands.guild_only()
    @app_commands.command(name="끄기", description="방송 알림을 비활성화합니다. 고유 알림 ID가 없으면 모든 알림을 비활성화합니다.")
    @app_commands.describe(alert_uuid="고유 알림 ID")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def _alert_disable(self, interaction: discord.Interaction, alert_uuid: typing.Optional[str]) -> None:
        with DB().getSession() as session:
            statements = session.query(
                Guild).filter_by(guild_id=interaction.guild.id).all()
            if alert_uuid != None and alert_uuid != '':
                for statement in statements:
                    if statement.uuid == alert_uuid:
                        statements = statement
                        break
            if statements == None:
                await interaction.response.send_message("방송 알림이 설정되어있지 않습니다.")
                return
            else:
                if alert_uuid != None and alert_uuid != '':
                    statements.activated = False
                    session.commit()
                else:
                    for statement in statements:
                        statement.activated = False
                        session.commit()
            await interaction.response.send_message(f"방송 알림{'' if alert_uuid != None and alert_uuid != '' else '들'}을 비활성화하였습니다.")

    @app_commands.guild_only()
    @app_commands.command(name="켜기", description="방송 알림을 활성화합니다. 고유 알림 ID가 없으면 모든 알림을 비활성화합니다.")
    @app_commands.describe(alert_uuid="고유 알림 ID")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def _alert_enable(self, interaction: discord.Interaction, alert_uuid: typing.Optional[str]) -> None:
        with DB().getSession() as session:
            statements = session.query(
                Guild).filter_by(guild_id=interaction.guild.id).all()
            if alert_uuid != None and alert_uuid != '':
                for statement in statements:
                    if statement.uuid == alert_uuid:
                        statements = statement
                        break
            if statements == None:
                await interaction.response.send_message("방송 알림이 설정되어있지 않습니다.")
                return
            else:
                if alert_uuid != None and alert_uuid != '':
                    statements.activated = True
                    session.commit()
                else:
                    for statement in statements:
                        statement.activated = True
                        session.commit()
            await interaction.response.send_message(f"방송 알림{'' if alert_uuid != None and alert_uuid != '' else '들'}을 활성화하였습니다.")

    @app_commands.guild_only()
    @app_commands.command(name="삭제", description="방송 알림 등록 정보를 삭제합니다. 고유 알림 ID가 없으면 모든 알림을 삭제합니다.")
    @app_commands.describe(alert_uuid="고유 알림 ID")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def _alert_delete(self, interaction: discord.Interaction, alert_uuid: typing.Optional[str]) -> None:
        with DB().getSession() as session:
            statements = session.query(
                Guild).filter_by(guild_id=interaction.guild.id).first()
            if alert_uuid != None and alert_uuid != '':
                for statement in statements:
                    if statement.uuid == alert_uuid:
                        statements = statement
                        break
            if statements == None:
                await interaction.response.send_message("방송 알림이 설정되어있지 않습니다.")
                return
            else:
                if alert_uuid != None and alert_uuid != '':
                    session.delete(statements)
                    session.commit()
                else:
                    for statement in statements:
                        session.delete(statement)
                        session.commit()
            await interaction.response.send_message(f"방송 알림{'' if alert_uuid != None and alert_uuid != '' else '들'}을 삭제하였습니다.")

    @app_commands.guild_only()
    @app_commands.command(name="정보", description="방송 알림 정보를 출력합니다.")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def _alert_info(self, interaction: discord.Interaction) -> None:
        with DB().getSession() as session:
            statements = session.query(
                Guild).filter_by(guild_id=interaction.guild.id).all()
            if statements == None or statements == []:
                await interaction.response.send_message("방송 알림이 설정되어있지 않습니다.")
                return
            else:
                async def get_page(page: int):
                    limit = 5
                    embed = discord.Embed(
                        title="ℹ️ 방송알림 등록 정보", description="현재 이 서버에 등록된 방송 알림 정보 입니다.", color=0x00ff00)
                    offset = (page-1) * limit
                    for statement in statements[offset:offset+limit]:

                        streamer_info = await self.fetch_streamer_info(statement.streamer_id)
                        streamer_info = streamer_info["content"]

                        if streamer_info["channelId"] is None:
                            await interaction.response.send_message("채널을 찾을 수 없습니다.")
                            return

                        stream_info_data = await self.fetch_stream_info(statement.streamer_id)
                        stream_info_data = stream_info_data["content"]

                        embed.add_field(
                            name=f"🔑 고유 알림 ID [``{statement.uuid}``]", value=f"채널: [{streamer_info['channelName']}](https://chzzk.naver.com/{statement.streamer_id})\n알림 채널: <#{statement.alert_channel}>\n알림 메세지: {statement.alert_text if statement.alert_text else '없음'}\n활성화 여부: {'활성화' if statement.activated else '비활성화'}", inline=False)
                    n = StreamAlertInfo.compute_total_pages(
                        len(statements), limit)
                    embed.set_footer(text=f"{page} / {n} 페이지")
                    return embed, n

                await StreamAlertInfo(interaction, get_page).navigate()

    @_set_stream_alert.error
    async def _set_stream_alert_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(content="이 명령어를 실행할 권한이 없는 것 같습니다.")

    @_alert_disable.error
    async def _alert_disable_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(content="이 명령어를 실행할 권한이 없는 것 같습니다.")

    @_alert_enable.error
    async def _alert_enable_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(content="이 명령어를 실행할 권한이 없는 것 같습니다.")

    @_alert_info.error
    async def _alert_info_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError) -> None:
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(content="이 명령어를 실행할 권한이 없는 것 같습니다.")


async def setup(bot: commands.Bot) -> None:
    session = aiohttp.ClientSession()
    cog = BroadcastGuildAlert(bot, session)
    await bot.add_cog(cog)
