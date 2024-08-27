import discord
from discord import app_commands
from discord import Embed
from discord import Color as c
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput, Select
import asyncio
from datetime import datetime
from datetime import datetime,timedelta, time
import random 
import re


class dm_tools(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="skill_check", description="Look up game information and lore")
    async def skill_check(self, interaction: discord.Integration, user: discord.User, skill: str, hidden: bool = False ):
        skill_check_emebed = Embed(title="Skill Check", description=f"{skill} check for {user.name}")

        skill_check_view = View()
        
        async def roll_callback(interaction: discord.Interaction):
            if user.id == interaction.user.id:
                pass
            else:
                skill_check_emebed.description = f"{skill} check for {user.id}\nUser is not {user.mention}. Please have have correct user roll"

                if hidden is False:
                    await interaction.response.send_message(embed=skill_check_emebed, ephemeral=True)
                else:
                    await interaction.response.send_message(embed=skill_check_emebed)

        roll_button = Button(label="Roll :die:", style=discord.ButtonStyle.green)
        skill_check_view.add_item(roll_button)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(dm_tools(client))
