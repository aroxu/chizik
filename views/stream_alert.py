from asyncio import sleep
import discord

from models.alert import Alert

BASE_URL = "https://api.chzzk.naver.com/service/v1/channels/"


class StreamAlertCreateConfirm(discord.ui.View):
    def __init__(self, timeout=15, **kwargs):
        self.interaction = kwargs["interaction"]
        self.channel_id = kwargs["channel_id"]
        self.alert_channel = kwargs["alert_channel"]
        self.alert_text = kwargs["alert_text"]
        super().__init__(timeout=timeout)

    @discord.ui.button(label="이대로 할레요", style=discord.ButtonStyle.success, custom_id="stream_alert_create_confirm")
    async def _alert_create_confirm(self, interaction: discord.Interaction, confirm_button: discord.ui.Button):
        try:
            guild, created = Alert.get_or_create(
                guild_id=interaction.guild.id, streamer_id=self.channel_id, alert_channel=self.alert_channel.id, alert_text=("" if self.alert_text == None else self.alert_text), is_streaming=True, activated=True
            )
            if not created:
                await interaction.response.edit_message(content="이미 해당 서버에 동일한 방송인의 알림이 설정되어 있습니다.", view=None, embed=None, delete_after=5)
                self.value = True
                self.stop()
                return
            await interaction.response.edit_message(content="방송 알림을 설정하였습니다.", view=None, embed=None, delete_after=5)
            self.value = True
            self.stop()
        except Exception as e:
            print(e)
            await interaction.response.edit_message(content="오류가 발생하였습니다.", view=None, embed=None, delete_after=5)
            self.value = True
            self.stop()

    @discord.ui.button(label="취소", style=discord.ButtonStyle.red, custom_id="stream_alert_cancel")
    async def _alert_create_cancel(self, interaction: discord.Interaction, cancel_button: discord.ui.Button):
        self.value = True
        self.stop()
        await interaction.response.edit_message(content="취소되었습니다.", view=None, embed=None, delete_after=5)

    async def on_timeout(self) -> None:
        timeout_message = await self.interaction.followup.send(content="시간이 초과되었습니다.")
        await sleep(5)
        await timeout_message.delete()
        return await super().on_timeout()
