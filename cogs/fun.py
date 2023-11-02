import discord
import random
import aiohttp
import os
import platform
import time
import json

from discord import app_commands
from discord.ext import commands
from discord.app_commands import AppCommandError

TOPGG_TOKEN = os.environ["TOPGG_TOKEN"]
NASA_TOKEN = os.environ["NASA_TOKEN"]


#COG CLASS
class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.discord_version = discord.__version__
        self.platform = platform.python_version()
        self.user_agent = f"Project Cozy/1.0 (discord.py {self.discord_version}; +https://projectcozy.xyz)"


async def setup(bot):
    await bot.add_cog(Fun(bot))