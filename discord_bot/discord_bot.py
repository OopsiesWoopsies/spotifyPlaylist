import discord, slash_commands
from discord.ext import commands
import logging

import os

bot_token = os.getenv("DISCORD_BOT_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
@bot.event
async def on_ready():
    try:
        # bot.tree.add_command(slash_commands.S(name="user", description="User related commands"))
        slash_commands.setup(bot)
        await bot.tree.sync(guild=slash_commands.GUILD_ID)
        print(f"I, {bot.user.name}, am ready")
    except Exception as e:
        print(f"FAILED {e}")

bot.run(bot_token, log_handler=handler, log_level=logging.DEBUG)