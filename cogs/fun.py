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
from datetime import timedelta
from aiohttp_client_cache import CachedSession, CacheBackend
from re import search

NASA_TOKEN = os.environ["NASA_TOKEN"]

cache = CacheBackend(expire_after=timedelta(seconds=120))

#COG CLASS
class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.discord_version = discord.__version__
        self.platform = platform.python_version()
        self.user_agent = f"Project Cozy/1.0 (discord.py {self.discord_version}; +https://projectcozy.xyz)"

    #COZYSTUFF COMMAND
    @app_commands.command(name="cozystuff", description="Cozy stuff on Reddit!")
    @app_commands.checks.cooldown(1, 5.0)
    async def cozystuff(self, interaction: discord.Interaction) -> None:
        subreddit = [
            'https://www.reddit.com/r/cozy/new.json?limit=100',
            'https://www.reddit.com/r/cozyplaces/new.json?limit=100'
        ] 

        async with CachedSession(cache=cache) as session:
            async with session.get(random.choice(subreddit)) as reddit:
                res = await reddit.json()
                while True:
                    counter = 0
                    random_post = res["data"]["children"][random.randint(0, 99)]
                    image_url = str(random_post["data"]["url"])
                    if search(".jpg|.jpeg|.png|.gif$", image_url):
                        break
                    else:
                        counter += 1
                        if counter == 100:
                            image_url = None
                            break

                permalink = random_post["data"]["permalink"]
                title = random_post["data"]["title"]
                subreddit_title = random_post["data"]["subreddit"]
                embed = discord.Embed(title=f"{title}", description="", url=f"https://reddit.com{permalink}", color=0xeb6123)
                embed.set_image(url=image_url)
                embed.set_footer(text=f"By r/{subreddit_title}")
                await interaction.followup.send(embed=embed)

    @cozystuff.error
    async def meme_error(self, interaction: discord.Interaction, error: AppCommandError) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            unixtime = int(time.time())
            totaltime = unixtime + int(error.retry_after)
            embed = discord.Embed(
                title="Slow down!",
                description=f"You can use this command again <t:{totaltime}:R>",
                color=0xb40000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    
    #ADVICE SLIP COMMAND
    @app_commands.command(name="advice", description="Get useful advice! By adviceslip.com")
    @app_commands.checks.cooldown(1, 5.0)
    async def advice(self, interaction: discord.Interaction):
        url = "https://api.adviceslip.com/advice"
        headers = {"Accept": "text/plain", "User-Agent": self.user_agent}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                answer = json.loads(await response.text())
                await interaction.response.send_message(f"{answer['slip']['advice']}")
    
    @advice.error
    async def advice_error(self, interaction: discord.Interaction, error: AppCommandError) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            unixtime = int(time.time())
            totaltime = unixtime + int(error.retry_after)
            embed = discord.Embed(
                title="Slow down!",
                description=f"You can use this command again <t:{totaltime}:R>",
                color=0xb40000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


    #APOD COMMAND
    @app_commands.command(name="astronomy", description="Do you find astronomy cool? This command is for you!")
    @app_commands.checks.cooldown(1, 10.0)
    async def astronomy(self, interaction: discord.Interaction):
        url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_TOKEN}"
        headers = {"Accept": "text/plain", "User-Agent": self.user_agent}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                answer = json.loads(await response.text())
                image_url = answer['hdurl']
                embed = discord.Embed(title=f"{answer['title']}", description="", color=0xb40000)
                embed.set_image(url=image_url)
                embed.set_footer(text=f"Date: {answer['date']}")
                await interaction.response.send_message(embed=embed)
    
    @astronomy.error
    async def apod_error(self, interaction: discord.Interaction, error: AppCommandError) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            unixtime = int(time.time())
            totaltime = unixtime + int(error.retry_after)
            embed = discord.Embed(
                title="Slow down!",
                description=f"You can use this command again <t:{totaltime}:R>",
                color=0xb40000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Fun(bot))