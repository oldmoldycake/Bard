import asyncio
import random 
import re



class roll_functions:
    def __init__(self) -> None:
        pass
    async def roll(self, roll= None, advantage_disadvantage = None, roll_option = None, roll_option_value = None, additional_roll_1 = None, additional_roll_2 = None, modifier = None, modifier_2 = None):
        roll = roll.upper()

        if "D" not in roll or roll.endswith("D"):
            #await interaction.response.send_message(f"Invalid Roll Format {roll}. Please format like \"2D20\" or \"1D6\".")
            return ["error",f"Invalid Roll Format {roll}. Please format like \"2D20\" or \"1D6\"."]
        
        if roll.startswith("D"):
            roll = "1" + roll
        
        rolls, sides = roll.split('D')

        if (additional_roll_1 is not None):
            additional_roll_1 = additional_roll_1.upper()
            if ("D" not in  additional_roll_1):
                #await interaction.response.send_message(f"Invalid Roll Format {additional_roll_1}. Please format like \"2D20\" or \"1D6\".")
                return ["error", f"Invalid Roll Format {additional_roll_1}. Please format like \"2D20\" or \"1D6\"."]

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
                #await interaction.response.send_message(f"Invalid Roll Format {additional_roll_2}. Please format like \"2D20\" or \"1D6\".")
                return ["error",f"Invalid Roll Format {additional_roll_2}. Please format like \"2D20\" or \"1D6\"."]
        
        
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
                #await interaction.response.send_message("Please only include one sign in modifier")
                return None
            elif len(parts) > 2:
                #await interaction.response.send_message("Please keep modifiy two parameter in \"+2\" formart.")
                return None
            
            modifier_sign, modifier_value = parts

        if modifier_2 is not None:
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
                #await interaction.response.send_message("Please only include one sign in modifier_2")
                return None
            elif len(parts) > 2:
                #await interaction.response.send_message("Please keep modifiy two parameter in \"+2\" formart.")
                return None
            modifier_2_sign, modifier_2_value = parts


        if roll_option not in ('exploding','keep_highest','drop_highest','keep_lowest','drop_lowest', None):
            #await interaction.response.send_message("Invalid roll option. Please select a valid option")
            return ["errror","Invalid roll option. Please select a valid option"]
        elif int(rolls) > 50:
            #await interaction.response.send_message("Please enter a roll value below fifty.")
            return ["errror","Please enter a roll value below fifty."]
        elif (roll_option_value is not None) and (roll_option_value < 0):
            #await interaction.response.send_message("Please enter a roll option value above one")
            return ["errror","Please enter a roll option value above one"]
        elif (roll_option_value is not None and self.is_not_round(roll_option_value)) or (modifier is not None and self.is_not_round(int(modifier_value))) or (modifier_2 is not None and self.is_not_round(int(modifier_2_value))):
            #await interaction.response.send_message("Please use whole numbers")
            return ["errror","Please use whole numbers"]
        elif (roll_option is not None and roll_option_value is None) and (roll_option not in ('exploding')):
            #await interaction.response.send_message("Missing roll option value. Please put a value and try again")
            return ["errror","Missing roll option value. Please put a value and try again"]
        elif (roll_option_value is not None and roll_option is None) and (roll_option not in ('exploding')):
            #await interaction.response.send_message("Missing roll option. Please select a roll option and try again")
            return ["errror",]
        elif (roll_option in ('keep_highest','drop_highest','keep_lowest','drop_lowest')) and (roll_option_value > int(sides)):
            #await  interaction.response.send_message("This option value can not be higher than number of dice rolls.")
            return ["errror","This option value can not be higher than number of dice rolls."]
        elif (additional_roll_1 is not None) and int(additional_roll_1_rolls) > 50:
            #await interaction.response.send_message("Please enter a additional_roll_1 value below fifty.")
            return ["errror","Please enter a additional_roll_1 value below fifty."]
        elif (additional_roll_2 is not None) and int(additional_roll_2_rolls) > 50:
            #await interaction.response.send_message("Please enter a additional_roll_2 value below fifty.")
            return ["errror","Please enter a additional_roll_2 value below fifty."]
        
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

            return ["success", roll_string, sum]                        

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
            return ["success", roll_string, sum]                        
