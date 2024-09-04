import discord
from discord import app_commands
from discord import Embed
from discord import Color as c
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput, Select
import asyncio
import random 
import re
import numpy as np
from dotenv import load_dotenv
import os

from cogs.modules.QueryHandler import QueryHandler


class utilities(commands.Cog):
    def __init__(self, bot: commands.Bot):

        self.bot = bot

    @app_commands.command(name="help", description="Help about varius aspect of the bot")
    async def skill_check(self, interaction: discord.Integration):
        help_embed = Embed(title="Bard help menu")

        help_embed.description = """
        roll: Used to roll dice with various modifications. To used saved values type the name of said mod in the modifier box or a number.
        set_mods: Allows you to set your modifiers values to be saved (open to more effective ways to do this).
        lookup: Will look on DnD beyond and teh forgotten realms wiki for your query. 
        skill_check: Allows DM to send a skill check for a player or the group. 
        help: If you are reading this i hope you know what this is.
        info: Info about the bot
        cat_pic: I just really like cat pics.
        """
    
    @app_commands.command(name="info", description="Info about the bot")
    async def skill_check(self, interaction: discord.Integration):
        info_embed = Embed(title="Bard Info")

        info_embed.description = """


            """



    @app_commands.command(name="cat_pic", descrption="cat images via TheCatAPI.")
    async def cat_pic(self, interaction: discord.Interaction):
        pass
    
async def setup(client:commands.Bot) -> None:
    await client.add_cog(utilities(client))

        