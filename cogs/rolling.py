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
import numpy as np
from cogs.modules.roll_functions import roll_functions as rf


class rolling(commands.Cog):
    def __init__(self, bot: commands.Bot):

        self.bot = bot
        self.rf = rf()
        

    @app_commands.command(name="roll", description="Used to make dice rolls")
    @app_commands.describe(
        roll = "The roll expression for the dice roll",
        roll_option = "Add various modifications to dice roll, All default to 1",
        roll_option_value = "The value for the selected roll options.",
        additional_roll_1 = "Lets you add another dice roll to the initial roll", 
        additional_roll_2 = "Lets you add another dice roll to the initial roll", 
        modifier = "Add/Subtract/Divide/Multiply a modifiery to your roll. Adds be default",
        modifier_2 = "Add/Subtract/Divide/Multiply a modifiery to your roll. Adds by default",
        hidden = "Hide the roll from other players. Off by deafult"
        )
    async def roll(self, interaction: discord.Interaction, roll:str,advantage_disadvantage: str = None, roll_option:str = None, roll_option_value:int = None, additional_roll_1:str = None, additional_roll_2:str = None, modifier:str = None, modifier_2:str = None, hidden: bool =  False):
        roll_result = await self.rf.roll(roll= roll, advantage_disadvantage = advantage_disadvantage, roll_option = roll_option, roll_option_value = roll_option_value, additional_roll_1 = additional_roll_1, additional_roll_2 = additional_roll_2, modifier = modifier, modifier_2 = modifier_2)
        print(roll_result)
        if roll_result[0] == "error":
            status, error_message = roll_result

            roll_error_embed = Embed(title=f"Error with roll {roll}")

            roll_error_embed.add_field(
                name="Error",
                value=error_message
            )
            if hidden:
                await interaction.response.send_message(embed=roll_error_embed, ephemeral=True)
            else:
                await interaction.response.send_message(embed=roll_error_embed)

        elif roll_result[0] == "success":
            status, roll_string, sum = roll_result

            roll_success_embed = Embed(title=f"Roll results for {roll} :die:")

            roll_success_embed.add_field(
                name="Roll",
                value=roll_string
            )

            roll_success_embed.add_field(
                name="Result",
                value=sum
            )
            if hidden:
                await interaction.response.send_message(embed=roll_success_embed, ephemeral=True)
            else:
                await interaction.response.send_message(embed=roll_success_embed)
                
    @roll.autocomplete("roll_option")
    async def autocomplete_callback(self, interaction: discord.Interaction, current: str):
      return [
        app_commands.Choice(name='Exploding Dice (If you roll the highest value on a die then keep rolling until you don\'t', value='exploding'),
        app_commands.Choice(name='Keep Highest (Keeps x highest dice. Defaults to 1)', value='keep_highest'),
        app_commands.Choice(name='Drop Highest (Drops x highest dice, Defaults to 1)', value='drop_highest'),
        app_commands.Choice(name='Keep Lowest (Keeps x lowest dice, Defaults to 1)', value='keep_lowest'),
        app_commands.Choice(name='Drop Lowest (Drops x lowest dice, Defaults to 1)', value='drop_lowest')
        ]
    
    @roll.autocomplete("advantage_disadvantage")
    async def autocomplete_callback(self, interaction: discord.Interaction, current: str):
      return [
        app_commands.Choice(name='Advantage (Rolls dice twice and keeps higher result)', value='advantage'),
        app_commands.Choice(name='Disadvantage (Rolls dice twice and keeps lower result)', value='disadvantage')
        ]

    async def search_in_file(self, filename, query):
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split('-')
                if len(parts) == 2 and query in parts[1]:
                    return line.strip()
        return None  # Return None if no match is found 


    
async def setup(client:commands.Bot) -> None:
    await client.add_cog(rolling(client))
