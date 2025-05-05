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

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    try:
        slash_commands.setup(bot)
        await bot.tree.sync(guild=slash_commands.GUILD_ID)
        print(f"I, {bot.user.name}, am ready")
    except Exception as e:
        print(f"FAILED {e}")


@bot.event
async def on_disconnect(): # If it needs to reconnect make it so it doesn't run setup again or sync
    print("BOT DISCONNECTED")
    user_tokens.write_json()
    print("SAVED")


def on_exit():
    user_tokens.write_json()
    print("SAVED")

atexit.register(on_exit)


bot.run(bot_token, log_handler=handler, log_level=logging.DEBUG)