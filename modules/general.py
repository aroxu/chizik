import os
import platform
import discord
from discord import app_commands
from discord.ext import commands
import psutil

import SECRETS


class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_unload(self) -> None:
        return await super().cog_unload()

    @app_commands.command(name="정보", description="봇 정보를 보여줍니다.")
    async def _bot_info(self, interaction: discord.Interaction) -> None:
        process = psutil.Process(os.getpid())
        mem = process.memory_percent()

        embed = discord.Embed(
            title="치직",
            description=f"봇 버전: **{SECRETS.version}**\n봇 개발자: **<@294146247512555521>(@aroxu)**", color=0x00fea5)
        embed.add_field(name="Discord 관련 정보",
                        value=f"서버 수: **{len(self.bot.guilds)}**\n핑: **{round(self.bot.latency * 1000)}ms**", inline=False)
        embed.add_field(
            name="호스트 정보", value=f"OS: {platform.platform()}\n봇의 CPU 사용량: {psutil.cpu_percent()}%\n봇의 RAM 사용량: {round(mem, 2)}%", inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    cog = General(bot)
    await bot.add_cog(cog)
