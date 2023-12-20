import asyncio
import logging
from pathlib import Path

import discord
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound

import SECRETS


class Chizik(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        intent = discord.Intents.default()
        super().__init__(command_prefix="", intents=intent, activity=discord.Activity(
            type=discord.ActivityType.listening, name="치지직.. 신호"))
        self.remove_command("help")

    async def setup_hook(self):
        self.loop.create_task(self.load_all_extensions())

    async def load_all_extensions(self):
        await self.wait_until_ready()
        await asyncio.sleep(1)
        commands = [x.stem for x in Path('modules').glob('*.py')]
        for extension in commands:
            try:
                await self.load_extension(f'modules.{extension}')
                print(f'{extension} 모듈을 성공적으로 로드하였습니다.')
            except Exception as e:
                error = f'{extension}\n {type(e).__name__} : {e}'
                print(f'로드 오류 발생:\n{error}')
            print('-' * 32)
        await self.tree.sync()

    async def on_ready(self):
        self.app_info = await self.application_info()
        print('-' * 32)
        print(f'{self.user.name}(으)로 로그인됨\n'
              f'Discord.py 버전: {discord.__version__}\n'
              f'소유자: {self.app_info.owner}\n'
              f'초대 링크: https://discord.com/oauth2/authorize?client_id={self.user.id}&scope=bot+applications.commands&permissions=149504')
        print('-' * 32)

    async def on_guild_join(self, guild):
        print(f'서버 {guild.name} ({guild.member_count}명의 유저)에 참가하였습니다!')

    async def on_command_error(self, ctx, reason):
        if isinstance(reason, CommandNotFound):
            return
        print(f'명령어 오류 발생:\n{reason}')


async def run():
    logging.basicConfig(level=logging.INFO)
    chizik = Chizik(config=SECRETS)
    await chizik.start(SECRETS.bot_token)

asyncio.run(run())
