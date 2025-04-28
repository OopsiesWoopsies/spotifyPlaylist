import discord, slash_commands
from discord.ext import commands
import logging

from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv("DISCORD_BOT_TOKEN")
GUILD_ID = discord.Object(id=1366142338342322397)

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
@bot.event
async def on_ready():
    await bot.tree.sync(guild=GUILD_ID)
    print(f"I, {bot.user.name}, am ready")

slash_commands.setup(bot, GUILD_ID)

bot.run(bot_token, log_handler=handler, log_level=logging.DEBUG)