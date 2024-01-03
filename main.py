import asyncio
from contextlib import asynccontextmanager
import logging
from pathlib import Path

import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from fastapi import FastAPI

from db.index import DB
from models.alert import Alert
from models.index import models
import SECRETS


class Chizik(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        intent = discord.Intents.default()
        intent.guilds = True
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


chizik = Chizik(config=SECRETS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(level=logging.INFO)
    DB().connect()
    DB().create_all(models)
    asyncio.ensure_future(chizik.start(SECRETS.bot_token))
    try:
        yield
    finally:
        await chizik.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/guilds")
async def guilds():
    result = []
    for guild in chizik.guilds:
        result.append({"id": guild.id, "name": guild.name})

    return result


@app.get("/guilds/{guild_id}")
async def guild(guild_id):
    guild = await chizik.fetch_guild(int(guild_id))
    print(guild)
    alerts = Alert.select().where(Alert.guild_id == guild_id)
    result = []
    for alert in alerts:
        result.append({
            "uuid": alert.uuid,
            "streamer_id": alert.streamer_id,
            "alert_channel": alert.alert_channel,
            "alert_text": alert.alert_text,
            "activated": alert.activated,
            "is_streaming": alert.is_streaming
        })
    return {"id": guild_id, "name": guild.name, "alert_info": result}
