import discord
from discord.ext import commands
from discord.ext import tasks
from typing import Literal, Optional, Union
from environs import Env
from utils import Color
#from utils import log, warn
#from utils import db
import aiohttp
import datetime
import os
import asyncio
import logging

env = Env()
env.read_env()

token = env.str("DSC_TOKEN")

root = logging.getLogger("discord")
root.setLevel(logging.DEBUG)

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

class Bot(commands.AutoShardedBot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    url: str
    gs: list
    gc: int
    mc: int
    time: str

    async def setup_hook(self) -> None:
        #self.uptime.start()

    async def on_ready(self) -> None:
        gs = bot.guilds
        gc = len(gs)
        mc = 0
        for g in gs:
            mc = mc + len(g.members)
        print(f"{Color.GREEN}[SUCCESS]{Color.CYAN} Logged in as {Color.BOLD}{self.user.name}{Color.RESET}{Color.CYAN} at ID {Color.BOLD}{self.user.id}{Color.RESET}{Color.CYAN}.\nIn {Color.BOLD}{gc}{Color.RESET}{Color.CYAN} guilds\nwith {Color.BOLD}{mc}{Color.RESET}{Color.CYAN} total members.\nShard count is {Color.BOLD}{self.shard_count}{Color.RESET}{Color.CYAN}.\nInvite: https://discord.com/api/oauth2/authorize?client_id={self.user.id}&permissions=8&scope=bot%20applications.commands{Color.RESET}")

    async def on_shard_ready(self, shard_id: int) -> None:
        time = datetime.datetime.now().isoformat()
        print(f"{Color.RESET}{Color.GRAY}{time} {Color.RESET}{Color.CYAN}- {Color.GREEN}[SUCCESS] {Color.CYAN}Shard ID {shard_id} ready.{Color.RESET}")

    async def on_shard_resumed(self, shard_id: int):
        time = datetime.datetime.now().isoformat()
        print(f"{Color.RESET}{Color.GRAY}{time} {Color.RESET}{Color.CYAN}- {Color.GREEN}[SUCCESS] {Color.CYAN}Shard ID {shard_id} resumed.{Color.RESET}")

    @tasks.loop(seconds=60)
    async def uptime(self) -> None:
        url = env.str("UPTIME_PING")
        url = url + str(round(self.latency * 1000))
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as resp:
                json = await resp.json()
                if not resp.ok:
                    warn(f"Failed to ping {url}, got response {json} with status code {resp.status}")
                    return
                log(f"Pinged {url}, got response {json} with status code {resp.status}")

    @uptime.before_loop
    async def uptime_before(self) -> None:
        log("Starting ping sequence...")
        await self.wait_until_ready()

bot = Bot(command_prefix=commands.when_mentioned_or("sentry$"), intents=discord.Intents.all(), help_command=None)

async def load():
    for cmd in os.listdir("./commands"):
        if cmd.endswith(".py"):
            try:
                await bot.load_extension(f"commands.{cmd[:-3]}")
                print(f"{Color.GREEN}[LOADED]{Color.RESET} Loaded command {cmd} successfully.")
            except Exception as e:
                print(f"{Color.RED}[ERROR]{Color.RESET} Could not load command {cmd} due to the following error:\n{e}")

    for evt in os.listdir("./events"):
        if evt.endswith(".py"):
            try:
                await bot.load_extension(f"events.{evt[:-3]}")
                print(f"{Color.GREEN}[LOADED]{Color.RESET} Loaded event {evt} successfully.")
            except Exception as e:
                print(f"{Color.RED}[ERROR]{Color.RESET} Could not load event {evt} due to the following error:\n{e}")

async def main():
    await load()
    #await db.connect()
    await bot.start(token)

async def db_close():
    await db.disconnect()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print(f"{Color.LBLUE}[INFO]{Color.RESET} Recieved close signal, closing connection...")
    #asyncio.run(db_close())