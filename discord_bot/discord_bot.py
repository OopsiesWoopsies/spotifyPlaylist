import discord, slash_commands
from discord.ext import commands
import logging

from utils import user_tokens

import os
import atexit

bot_token = os.getenv("DISCORD_BOT_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready() -> None:
    '''
    Sets up the Discord bot and syncs the tree commands.
    :return: None.
    '''

    try:
        slash_commands.setup(bot)
        await bot.tree.sync(guild=slash_commands.GUILD_ID)
    except Exception as e:
        print(f"FAILED {e}")


@bot.event
async def on_disconnect() -> None:
    '''
    Writes to the .json file if the bot disconnects. Saves data.
    :return: None.
    '''

    user_tokens.write_json()


def on_exit():
    '''
    Writes to the .json file if the program shuts off. Saves data.
    :return: None.
    '''

    user_tokens.write_json()


if __name__ == "__main__":
    # Checks if the user exits the program.
    atexit.register(on_exit)
    bot.run(bot_token, log_handler=handler, log_level=logging.DEBUG)