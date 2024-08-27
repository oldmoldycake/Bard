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


class rolling(commands.Cog):
    def __init__(self, bot: commands.Bot):

        self.bot = bot
            
    async def get_var_name(self, var):
        for name, value in locals().items():
            if value is var:
                return name
        return None  # Variable not found in local scope
    
    def is_not_round(self, number):
          return number % 1 != 0
    
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
        roll = roll.upper()

        if "D" not in roll or roll.endswith("D"):
            await interaction.response.send_message(f"Invalid Roll Format {roll}. Please format like \"2D20\" or \"1D6\".")
            return None
        
        if roll.startswith("D"):
            roll = "1" + roll
        
        rolls, sides = roll.split('D')

        if (additional_roll_1 is not None):
            additional_roll_1 = additional_roll_1.upper()
            if ("D" not in  additional_roll_1):
                await interaction.response.send_message(f"Invalid Roll Format {additional_roll_1}. Please format like \"2D20\" or \"1D6\".")
                return None

        if (additional_roll_1 is not None):
            if additional_roll_1.startswith("D"):
                additional_roll_1 = "1" + additional_roll_1 
            additional_roll_1_rolls, additional_roll_1_sides = additional_roll_1.split('D')

            additional_roll_1_results = []

            additional_roll_1_sum = 0 
            for i in range(int(additional_roll_1_rolls)):
                additional_roll_1_result = random.randint(1,int(additional_roll_1_sides))
                additional_roll_1_results.append(additional_roll_1_result)
                additional_roll_1_sum = additional_roll_1_sum + additional_roll_1_result



        if (additional_roll_2 is not None):
            additional_roll_2 =additional_roll_2.upper()
            if "D" not in  additional_roll_2:
                await interaction.response.send_message(f"Invalid Roll Format {additional_roll_2}. Please format like \"2D20\" or \"1D6\".")
                return None
        
        
        if (additional_roll_2 is not None):
            if additional_roll_2.startswith("D"):
                additional_roll_2 = "1" + additional_roll_2 
            additional_roll_2_rolls, additional_roll_2_sides = additional_roll_2.split('D') 
            
            additional_roll_2_results = []

            additional_roll_2_sum = 0 
            for i in range(int(additional_roll_2_rolls)):
                additional_roll_2_result = random.randint(1,int(additional_roll_2_sides))
                additional_roll_2_results.append(additional_roll_2_result)
                additional_roll_2_sum = additional_roll_2_sum + additional_roll_2_result
        
        if modifier is not None:
            parts = []
            if (modifier.startswith("+")) or modifier.startswith("-") or modifier.startswith("*") or modifier.startswith("/"):
                parts = re.split(r"(?<=[\+\-\*\/])|(?=[\+\-\*\/])", modifier)
                parts = [part.strip() for part in parts if part.strip()] 
            else:
                parts.append("+")
                parts.append(modifier)

            sign_count = 0
            for part in parts:
                if part in ("+","-","/","*"):
                    sign_count+= 1

            if sign_count > 1:
                await interaction.response.send_message("Please only include one sign in modifier")
                return None
            elif len(parts) > 2:
                await interaction.response.send_message("Please keep modifiy two parameter in \"+2\" formart.")
                return None
            
            modifier_sign, modifier_value = parts

        if modifier_2 is not None:
            parts = []
            if (modifier_2.startswith("+")) or modifier_2.startswith("-") or modifier_2.startswith("*") or modifier_2.startswith("/"):
                    parts = re.split(r"(?<=[\+\-\*\/])|(?=[\+\-\*\/])", modifier)
                    parts = [part.strip() for part in parts if part.strip()] 
            else:
                parts.append("+")
                parts.append(modifier_2)modifier

            sign_count = 0
            if part in ("+","-","/","*"):
                    sign_count+= 1
            if sign_count > 1:
                await interaction.response.send_message("Please only include one sign in modifier_2")
                return None
            elif len(parts) > 2:
                await interaction.response.send_message("Please keep modifiy two parameter in \"+2\" formart.")
                return None
            modifier_2_sign, modifier_2_value = parts


        if roll_option not in ('exploding','keep_highest','drop_highest','keep_lowest','drop_lowest', None):
            await interaction.response.send_message("Invalid roll option. Please select a valid option")
            return None
        elif int(rolls) > 50:
            await interaction.response.send_message("Please enter a roll value below fifty.")
            return None
        elif (roll_option_value is not None) and (roll_option_value < 0):
            await interaction.response.send_message("Please enter a roll option value above one")
            return None
        elif (roll_option_value is not None and self.is_not_round(roll_option_value)) or (modifier is not None and self.is_not_round(int(modifier_value))) or (modifier_2 is not None and self.is_not_round(int(modifier_2_value))):
            await interaction.response.send_message("Please use whole numbers")
            return None
        elif (roll_option is not None and roll_option_value is None) and (roll_option not in ('exploding')):
            await interaction.response.send_message("Missing roll option value. Please put a value and try again")
            return None
        elif (roll_option_value is not None and roll_option is None) and (roll_option not in ('exploding')):
            await interaction.response.send_message("Missing roll option. Please select a roll option and try again")
            return None
        elif (roll_option in ('keep_highest','drop_highest','keep_lowest','drop_lowest')) and (roll_option_value > int(sides)):
            await  interaction.response.send_message("This option value can not be higher than number of dice rolls.")
            return None
        elif (additional_roll_1 is not None) and int(additional_roll_1_rolls) > 50:
            await interaction.response.send_message("Please enter a additional_roll_1 value below fifty.")
            return None
        elif (additional_roll_2 is not None) and int(additional_roll_2_rolls) > 50:
            await interaction.response.send_message("Please enter a additional_roll_2 value below fifty.")
            return None
        
        if advantage_disadvantage is not None and (advantage_disadvantage == 'disadvantage' or advantage_disadvantage == 'advantage'):
            roll_results = []
            roll_string = ""
            sum = 0

            for i in range(int(rolls)):
                dice_roll_pair = np.random.randint(1, int(sides) + 1, size=2)

                higher_roll = np.max(dice_roll_pair)
                lower_roll = np.min(dice_roll_pair)
                roll_results.append({"high": higher_roll, "low": lower_roll})

            # Apply roll options after generating all rolls
            if roll_option == 'keep_highest':
                roll_results = sorted(roll_results, key=lambda x: x['high'], reverse=True)[:roll_option_value]
            elif roll_option == 'drop_highest':
                roll_results = sorted(roll_results, key=lambda x: x['high'])[:int(rolls) - roll_option_value]
            elif roll_option == 'keep_lowest':
                roll_results = sorted(roll_results, key=lambda x: x['low'])[:roll_option_value]
            elif roll_option == 'drop_lowest':
                roll_results = sorted(roll_results, key=lambda x: x['low'], reverse=True)[:int(rolls) - roll_option_value]

            # Now calculate the sum and build the string
            for result in roll_results:
                if advantage_disadvantage == 'advantage':
                    sum += result['high']
                    roll_string += f'**{result["high"]}** ({result["low"]}) +'
                else:  # disadvantage
                    sum += result['low']
                    roll_string += f'**{result["low"]}** ({result["high"]}) +'
            roll_string = roll_string.rstrip('+')

            if additional_roll_1 is not None:
                sum = sum + additional_roll_1_sum
                additional_roll_1_string = ""
                for additional_roll_1_result in additional_roll_1_results:
                    additional_roll_1_string = additional_roll_1_string + f" + **{additional_roll_1_result}**"
                roll_string = roll_string + additional_roll_1_string

            if additional_roll_2 is not None:
                sum = sum + additional_roll_2_sum
                
                additional_roll_2_string = ""
                for additional_roll_2_result in additional_roll_2_results:
                    additional_roll_2_string = f" + **{additional_roll_2_result}**"
                roll_string = roll_string + additional_roll_2_string
            
            if modifier is not None:
                if modifier_sign == "+":
                    sum = sum + int(modifier_value)
                elif modifier_sign == "-":
                    sum = sum - int(modifier_value)
                elif modifier_sign == "/":
                    sum = round(sum/int(modifier_value))
                elif modifier_sign == "*":
                    sum = sum * int(modifier_value)
                roll_string = roll_string +  " " + modifier_sign + " " + f"**{modifier_value}**"

            if modifier_2 is not None:
                if modifier_2_sign == "+":
                    sum = sum + int(modifier_2_value)
                elif modifier_2_sign == "-":
                    sum = sum - int(modifier_2_value)
                elif modifier_2_sign == "/":
                    sum = round(sum/int(modifier_2_value))
                elif modifier_2_sign == "*":
                    sum = sum * modifier_2_value
                roll_string = roll_string +  " " + modifier_2_sign + " " + f"**{modifier_2_value}**"
            roll_embed = Embed(title=f"Advantage Roll Results ({rolls}D{sides}) 🎲")
                        
            roll_embed.add_field(
                name="Rolls",
                value=f"{roll_string}"
            )

            roll_embed.add_field(modifier

        else:
            roll_results = []
            roll_string = ""
            sum = 0

            for i in range(int(rolls)):
                die_roll = random.randint(1,int(sides))
                roll_results.append(int(die_roll))
                roll_string += f"{die_roll}, "


            # Apply roll options
            if roll_option == 'keep_highest':
                roll_results = sorted(roll_results, reverse=True)[:roll_option_value]
                for roll in roll_results:
                    sum = sum + int(roll)
                roll_string = "+ ".join(str(r) for r in roll_results)
            elif roll_option == 'drop_highest':
                roll_results = sorted(roll_results)[:int(rolls) - roll_option_value]
                for roll in roll_results:
                    sum = sum + int(roll)
                roll_string = "+ ".join(str(r) for r in roll_results)
            elif roll_option == 'keep_lowest':
                roll_results = sorted(roll_results)[:roll_option_value]
                for roll in roll_results:
                    sum = sum + int(roll)
                roll_string = "+ ".join(str(r) for r in roll_results)
            elif roll_option == 'drop_lowest':
                roll_results = sorted(roll_results, reverse=True)[:int(rolls) - roll_option_value]
                for roll in roll_results:
                    sum = sum + int(roll)
                roll_string = "+ ".join(str(r) for r in roll_results)

            if additional_roll_1 is not None:
                sum = sum + additional_roll_1_sum
                additional_roll_1_string = ""
                for additional_roll_1_result in additional_roll_1_results:
                    additional_roll_1_string = additional_roll_1_string + f" + {additional_roll_1_result}"
                roll_string = roll_string + additional_roll_1_string

            if additional_roll_2 is not None:
                sum = sum + additional_roll_2_sum
                
                additional_roll_2_string = ""
                for additional_roll_2_result in additional_roll_2_results:
                    additional_roll_2_string = f" + {additional_roll_2_result}"
                roll_string = roll_string + additional_roll_2_string
            
            if modifier is not None:
                if modifier_sign == "+":
                    sum = sum + int(modifier_value)
                elif modifier_sign == "-":
                    sum = sum - int(modifier_value)
                elif modifier_sign == "/":
                    sum = round(sum/int(modifier_value))
                elif modifier_sign == "*":
                    sum = sum * int(modifier_value)
                roll_string = roll_string +  " " + modifier_sign + " " + modifier_value

            if modifier_2 is not None:
                if modifier_2_sign == "+":
                    sum = sum + int(modifier_2_value)
                elif modifier_2_sign == "-":
                    sum = sum - int(modifier_2_value)
                elif modifier_2_sign == "/":
                    sum = round(sum/int(modifier_2_value))
                elif modifier_2_sign == "*":
                    sum = sum * modifier_2_value
                roll_string = roll_string +  " " + modifier_2_sign + " " + modifier_2_value
            roll_embed = Embed(title=f"Roll Results ({rolls}D{sides}) 🎲")
                        
            roll_embed.add_field(
                name="Rolls",
                value=f"{roll_string}"
            )

            roll_embed.add_field(
                name="Result",
                value=sum
            )
            await interaction.response.send_message(embed=roll_embed)    
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

    @app_commands.command(name="lookup", description="Look up game information and lore")
    @app_commands.describe(
        query = "The roll expression for the dice roll"
        )
    
    async def lookup(self, interaction: discord.Interaction, category: str, query:str= None):
        lookup_emebd = Embed(title="Lookup Results :mag:")

        if query is not None:
            lookup_emebd.description = f"Looking for **{query}** in **{category}**"

            query = query.lower()
            formatted_query_1 = query.replace(" ", "-")
            formatted_query_2 = query.replace(" ", "_")

            if category == 'races':
                if query in ('dragonborn', 'dwarf','elf','gnome','half-elf','half-orc','halfling','human','tiefling'):
                    dnd_beyond_link = f"https://www.dndbeyond.com/races/{formatted_query_1}"
                    lookup_emebd.add_field(name="DnD Beyond", value=f"[Link]({dnd_beyond_link})")
                else:
                    dnd_beyond_link = "https://www.dndbeyond.com/races/"
                    
                    search = await self.search_in_file("/home/oldmoldycake/bard_bot/cogs/races.txt", query=formatted_query_1)
                    if search is not None:
                        dnd_beyond_link = dnd_beyond_link + search
                        lookup_emebd.add_field(name="DnD Beyond", value=f"[Link]({dnd_beyond_link})")
                    else:
                        dnd_beyond_link = dnd_beyond_link + formatted_query_1
                        lookup_emebd.add_field(name="DnD Beyond", value=f"[Link]({dnd_beyond_link})")
                        
            elif category in ('classes', 'backgrounds', 'feats','spells','equipment','magic-items','monsters'):
                formatted_query_1 = query.replace(" ", "-")
                dnd_beyond_link = f"https://www.dndbeyond.com/{category}/{formatted_query_1}"
                lookup_emebd.add_field(name="DnD Beyond", value=f"[Link]({dnd_beyond_link})")

            forgotten_realms_wiki_link = f"https://forgottenrealms.fandom.com/wiki/{formatted_query_2}"
            lookup_emebd.add_field(name="Forgotten Realms Wiki", value=f"[Link]({forgotten_realms_wiki_link})")

            await interaction.response.send_message(embed=lookup_emebd)
        else:
            lookup_emebd.description = f"Looking for **{category}**"

            dnd_beyond_link = f"https://www.dndbeyond.com/{category}"
            
            lookup_emebd.add_field(name="DnD Beyond", value="[Link]({dnd_beyond_link})")

            if category in ('races', 'classes', 'spells', 'magic-items', 'monsters'):
                if category == 'races':
                    forgotten_realms_wiki_link = "https://forgottenrealms.fandom.com/wiki/Category:races"
                elif category == 'classes':
                    forgotten_realms_wiki_link = "https://forgottenrealms.fandom.com/wiki/Category:races"
                elif category == 'spells':
                    forgotten_realms_wiki_link = "https://forgottenrealms.fandom.com/wiki/Category:spells"
                elif category == 'magic-items':
                    forgotten_realms_wiki_link = "https://forgottenrealms.fandom.com/wiki/Category:Magic_items"
                elif category == 'monsters':
                    forgotten_realms_wiki_link = "https://forgottenrealms.fandom.com/wiki/Category:Creatures"

                lookup_emebd.add_field(name="Forgotten Realms Wiki", value=f"[Link]({forgotten_realms_wiki_link}")
            else:
                pass

            await interaction.response.send_message(embed=lookup_emebd)

    @lookup.autocomplete("category")
    async def autocomplete_callback(self, interaction: discord.Interaction, current: str):
      return [
        app_commands.Choice(name='Races', value='races'),
        app_commands.Choice(name='Classes', value='classes'),
        app_commands.Choice(name='Backgrounds', value='backgrounds'),
        app_commands.Choice(name='Feats', value='feats'),
        app_commands.Choice(name='Spells', value='spells'),
        app_commands.Choice(name='Equipment', value='equipment'),
        app_commands.Choice(name='Magic Items', value='magic-items'),
        app_commands.Choice(name='Monsters', value='monsters')
        ]
    
async def setup(client:commands.Bot) -> None:
    await client.add_cog(rolling(client))
