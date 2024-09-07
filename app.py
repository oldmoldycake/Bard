import discord
from discord.ext import commands
from discord import app_commands
from colorama import Back, Fore, Style
import time
import platform
from dotenv import load_dotenv
import os

#super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=discord.Intents().all())
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())
cogslist = ['cogs.rolling', 'cogs.dm_tools', 'cogs.player_tools', 'cogs.utilites']


@bot.event
async def setup_hook():
    for ext in cogslist:
        await bot.load_extension(ext) 

@bot.event
async def on_ready():
    prfx = (Back.BLACK + Fore.GREEN + time.strftime("%H:%M:%S UTC", time.gmtime()) + Back.RESET + Fore.WHITE + Style.BRIGHT)
    print(prfx + " Logged in as " + Fore.YELLOW + bot.user.name)
    print(prfx + " Bot ID " + Fore.YELLOW + str(bot.user.id))
    print(prfx + " Discord Version " + Fore.YELLOW + discord.__version__)
    print(prfx + " Python Version " + Fore.YELLOW + str(platform.python_version()))
    synced = await bot.tree.sync()
    print(prfx + " Slash CMDs Synced " + Fore.YELLOW + str(len(synced)) + " Commands")

        
load_dotenv('/home/oldmoldycake/keys/keys.env') 
DISCORD_TOKEN = os.getenv("bard_token")
bot.run(DISCORD_TOKEN)   