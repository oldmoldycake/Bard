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

from cogs.modules.roll_functions import roll_functions as rf

class dm_tools(commands.Cog):
    def __init__(self, bot: commands.Bot): 
        self.bot = bot
        self.rf = rf()

    @app_commands.command(name="skill_check", description="Look up game information and lore")
    @app_commands.describe(
        type="The type of skill check this will be",
        difficulty_class="The threshhold needed to pass this roll",
        user="If selecting a user to roll this check",
        advantage_disadvantage="Determine if the roll will be advantage or disadvantage",
        additional_roll_1 = "Lets you add another dice roll to the initial roll", 
        additional_roll_2 = "Lets you add another dice roll to the initial roll", 
        modifier = "Add/Subtract/Divide/Multiply a modifiery to your roll. Adds be default",
        modifier_2 = "Add/Subtract/Divide/Multiply a modifiery to your roll. Adds by default",
        hidden = "Hide the roll from other players. Off by deafult"
        )
    async def skill_check(self, interaction: discord.Integration, type: str, difficulty_class: int, user: discord.User = None, hidden: bool = False, advantage_disadvantage: str = None, additional_roll_1:str =None, additional_roll_2: str =None, modifier: str =None, modifier_2: str =None, group: bool = False): 
        if user is not None:
            skill_check_emebed = Embed(title="Skill Check", description=f"{type} check for {user.name}")
        else:
            skill_check_emebed = Embed(title="Skill Check", description=f"{type}")

        skill_check_view = View()

        async def roll_callback(interaction: discord.Interaction):
            if user is None or user.id == interaction.user.id:
                skill_check_emebed.description = f"{type} roll with {difficulty_class} difficulty class"

                results = await self.rf.roll(roll="2D20", advantage_disadvantage=advantage_disadvantage, roll_option=None, roll_option_value=None, additional_roll_1=additional_roll_1, additional_roll_2= additional_roll_2, modifier=modifier, modifier_2=modifier_2)
                if results[0] == "error":
                    skill_check_emebed.description = f"Error with roll function.\nIf you see this please open a issue on [Github](https://github.com/oldmoldycake/Bard).\nPlease copy the exact command you sent to trigger this so that I can look into an fix it."
                    await interaction.response.send_message
                    return
                    
                status, roll_string, roll_result = results

                
            else:
                skill_check_emebed.description = f"{type} roll with {difficulty_class} difficulty class\nUser is not {user.mention}. Please have have correct user roll"

                if hidden is False:
                    await interaction.response.send_message(embed=skill_check_emebed, ephemeral=True)
                else:
                    await interaction.response.send_message(embed=skill_check_emebed)


        skill_check_emebed.description = f"{type} roll with {difficulty_class} difficulty class"
        roll_button = Button(label="Roll 🎲", style=discord.ButtonStyle.green)  # Use Unicode for the game die
        roll_button.callback = roll_callback

        skill_check_view.add_item(roll_button)

        await interaction.response.send_message(embed=skill_check_emebed, view=skill_check_view)

    @skill_check.autocomplete("type")
    async def autocomplete_callback(self, interaction: discord.Interaction, current: str):
        column_names = [
            'Strength', 'Dexterity', 'Constitution', 'Intelligence', 
            'Wisdom', 'Charisma', 'Acrobatics', 'Animal Handling', 'Arcana', 
            'Athletics', 'Deception', 'History', 'Insight', 'Intimidation', 
            'Investigation', 'Medicine', 'Perception', 'Performance', 'Persuasion', 
            'Religion', 'Slight of Hand', 'Stealth', 'Survival'
        ]

        # Filter based on what the user is typing
        matching_choices = [
            app_commands.Choice(name=col, value=col) 
            for col in column_names if current.lower() in col.lower()
        ]

        return matching_choices
    
    @skill_check.autocomplete("advantage_disadvantage")
    async def autocomplete_callback(self, interaction: discord.Interaction, current: str):
      return [
        app_commands.Choice(name='Advantage (Rolls dice twice and keeps higher result)', value='advantage'),
        app_commands.Choice(name='Disadvantage (Rolls dice twice and keeps lower result)', value='disadvantage')
        ]

async def setup(client:commands.Bot) -> None:
    await client.add_cog(dm_tools(client))
