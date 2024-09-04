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



class roll_functions:
    def __init__(self) -> None:
        load_dotenv('/home/oldmoldycake/keys/keys.env') 

        db_host = os.getenv("db_host")
        db_username = os.getenv("db_username")
        db_password = os.getenv("db_password")

        self.db_name = os.getenv("db_name")
        self.db_data_table_name = os.getenv("db_data_table_name")
        self.DATABASE_CONFIG = {
            'host': db_host,
            'user': db_username,
            'password': db_password,
        }

        self.QH = QueryHandler(self.DATABASE_CONFIG)

    async def get_var_name(self, var):
        for name, value in locals().items():
            if value is var:
                return name
        return None  # Variable not found in local scope
    
    async def is_not_round(self, number):
          return number % 1 != 0
    
    async def roll(self, interaction: discord.Interaction, roll= None, advantage_disadvantage = None, roll_option = None, roll_option_value = None, additional_roll_1 = None, additional_roll_2 = None, modifier = None, modifier_2 = None):
        roll = roll.upper()
        dnd_mods = ('strength', 'dexterity', 'constitution', 'intelligence', 
            'wisdom', 'charisma', 'acrobatics', 'animal handling', 'arcana', 
            'athletics', 'deception', 'history', 'insight', 'intimidation', 
            'investigation', 'medicine', 'perception', 'performance', 'persuasion', 
            'religion', 'slight of hand', 'stealth', 'survival')
        
        if "D" not in roll or roll.endswith("D"):
            return ["error",f"Invalid Roll Format {roll}. Please format like \"2D20\" or \"1D6\"."]
        
        if roll.startswith("D"):
            roll = "1" + roll
        
        split_roll = roll.split('D')

        if len(split_roll) > 2:
            return ["error", "Please only include one D"]
        else:
            rolls, sides =  split_roll
        if (additional_roll_1 is not None):
            additional_roll_1 = additional_roll_1.upper()
            if ("D" not in  additional_roll_1):
                return ["error", f"Invalid Roll Format {additional_roll_1}. Please format like \"2D20\" or \"1D6\"."]

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
            additional_roll_2 = additional_roll_2.upper()
            if ("D" not in  additional_roll_2):
                return ["error", f"Invalid Roll Format {additional_roll_2}. Please format like \"2D20\" or \"1D6\"."]

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
            if modifier.lower() in dnd_mods:
                results = self.QH.SQL(self.db_name, f"SELECT {modifier} FROM {self.db_data_table_name} WHERE user_id = {interaction.user.id}")

                if len(results) == 0:
                    return ["error",f"Please set your modifiers first"]

                print(result)
                modifier = results[0][0]
            elif not modifier.isdigit():
                return ["error", f"Please enter a valid modifier value"]
            

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
                return None
            elif len(parts) > 2:
                return None
            
            modifier_sign, modifier_value = parts

        if modifier_2 is not None:
            if modifier_2.lower() in dnd_mods:
                results = self.QH.SQL(self.db_name, f"SELECT {modifier_2} FROM {self.db_data_table_name} WHERE user_id = {interaction.user.id}")

                if modifier is None:
                    return ["error",f"Please set your modifiers first"]
                
                modifier = results[0][0]

            elif not modifier_2.isdigit():
                return ["error", f"Please enter a valid modifier_2 value"]

            parts = []
            if (modifier_2.startswith("+")) or modifier_2.startswith("-") or modifier_2.startswith("*") or modifier_2.startswith("/"):
                    parts = re.split(r"(?<=[\+\-\*\/])|(?=[\+\-\*\/])", modifier)
                    parts = [part.strip() for part in parts if part.strip()] 
            else:
                parts.append("+")
                parts.append(modifier_2)

            sign_count = 0
            if part in ("+","-","/","*"):
                    sign_count+= 1
            if sign_count > 1:
                return None
            elif len(parts) > 2:
                return None
            modifier_2_sign, modifier_2_value = parts

        if roll_option not in ('exploding','keep_highest','drop_highest','keep_lowest','drop_lowest', None):
            return ["error","Invalid roll option. Please select a valid option"]
        elif not rolls.isdigit():
            return ["error", "Please make sure total rolls in a number"] 
        elif int(rolls) > 50:
            return ["error","Please enter a roll value below fifty."]
        elif (roll_option_value is not None) and (roll_option_value < 0):
            return ["error","Please enter a roll option value above one"]
        elif (roll_option_value is not None and await self.is_not_round(roll_option_value)) or (modifier is not None and  await self.is_not_round(int(modifier_value))) or (modifier_2 is not None and await self.is_not_round(int(modifier_2_value))):
            return ["error","Please use whole numbers"]
        elif (roll_option is not None and roll_option_value is None) and (roll_option not in ('exploding')):
            return ["error","Missing roll option value. Please put a value and try again"]
        elif (roll_option_value is not None and roll_option is None) and (roll_option not in ('exploding')):
            return ["error","Missing roll option. Please select a roll option and try again"]
        elif (roll_option in ('keep_highest','drop_highest','keep_lowest','drop_lowest')) and (roll_option_value > int(sides)):
            return ["error","This option value can not be higher than number of dice rolls."]
        elif (additional_roll_1 is not None) and int(additional_roll_1_rolls) > 50:
            return ["error","Please enter a additional_roll_1 value below fifty."]
        elif (additional_roll_2 is not None) and int(additional_roll_2_rolls) > 50:
            return ["error","Please enter a additional_roll_2 value below fifty."]

        
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
                    additional_roll_2_string = additional_roll_2_string + f" + **{additional_roll_2_result}**"
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

            return ["success", roll_string, sum]                        

        else:
            roll_results = []
            roll_string = ""
            sum = 0

            for i in range(int(rolls)):
                die_roll = random.randint(1,int(sides))
                roll_results.append(int(die_roll))
                roll_string += f"{die_roll} + "
            roll_string = roll_string.rstrip(' + ')


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
                    additional_roll_2_string = additional_roll_2_string + f" + {additional_roll_2_result}"
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

            for chosen_roll in roll_results:
                sum = sum + int(chosen_roll)

            return ["success", roll_string, sum]                        

