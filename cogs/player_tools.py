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
from dotenv import load_dotenv
import os
from cogs.modules.roll_functions import roll_functions as rf
from cogs.modules.QueryHandler import QueryHandler


class player_tools(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        load_dotenv('/home/oldmoldycake/keys/keys.env') 

        db_host = os.getenv("db_host")
        db_username = os.getenv("db_username")
        db_password = os.getenv("db_password")

        self.db_name = os.getenv("db_name")
        self.db_data_table_name = os.getenv("db_data_table_name")
        self.DATABASE_CONFIG = {
            'host': 'localhost',
            'user': 'oldmoldycake',
            'password': '1229Bogging123123!',
        }

        self.QH = QueryHandler(self.DATABASE_CONFIG)


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
            
            lookup_emebd.add_field(name="DnD Beyond", value=f"[Link]({dnd_beyond_link})")

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

                lookup_emebd.add_field(name="Forgotten Realms Wiki", value=f"[Link]({forgotten_realms_wiki_link})")
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

    @app_commands.command(name="set_mods", description="Look up game information and lore")
    @app_commands.describe(
        modifier = "The modifier being set to a new values",
        value = "The value the modifier is being set too"
        )
    
    async def set_mods(self, interaction: discord.Interaction, modifier: str, value: int):
        user_info = self.QH.SQL(self.db_name, f"SELECT {interaction.user.id}, {modifier} FROM user_data WHERE user_id = {interaction.user.id}")

        if len(user_info) == 0:
            self.QH.SQL(self.db_name, f"INSERT INTO user_data (user_id, {modifier}) VALUES ({interaction.user.id},{value})")
            print(f"INSERT INTO user_data (user_id, {modifier}) VALUES ({interaction.user.id},{value})")

        else:
            print(user_info)
            user_id, current_modifier_value = user_info[0]

            self.QH.SQL(self.db_name, f"UPDATE {self.db_data_table_name} SET {modifier} = {value} WHERE user_id = user_id")

        modifier_embed = Embed(title="Set modifier" , description=f"Modifier {modifier} set successfully")            
        await interaction.response.send_message(embed=modifier_embed)

    @set_mods.autocomplete("modifier")
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
            app_commands.Choice(name=col, value=col.lower()) 
            for col in column_names if current.lower() in col.lower()
        ]

        return matching_choices

async def setup(client:commands.Bot) -> None:
    await client.add_cog(player_tools(client))