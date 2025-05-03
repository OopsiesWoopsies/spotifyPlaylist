from discord.app_commands import guilds

from spotify_util_functions import get_token, user_functions

import discord
from discord import app_commands


spotify_token, spotify_expiry = get_token.get_token()
GUILD_ID = discord.Object(id=1366142338342322397)


class User(app_commands.Group):
    @app_commands.command(name="current-user", description="Check yourself out!")
    @app_commands.guilds(GUILD_ID)
    async def current_user(self, interaction: discord.Interaction):
        user_id = interaction.user.id  # check if id is in env file before printing (same for every user related slash command)
        print(user_id)
        await interaction.response.send_message(user_functions.get_current_user(spotify_token), ephemeral=True)

# @bot.tree.command(name="current_user", description="Check yourself out!", guild=GUILD_ID)
# async def current_user(interaction: discord.Interaction):
#     user_id = interaction.user.id # check if id is in env file before printing (same for every user related slash command)
#     print(user_id)
#     await interaction.response.send_message(user_functions.get_current_user(spotify_token),ephemeral=True)
#
# @bot.command(name="account", description="", guild=GUILD_ID)
# async def spotify_account(interaction: discord.Interaction, add: str):
#     pass
#
# @spotify_account.Group(name="add", description="Add your spotify account!", guild=GUILD_ID)
# async def add_spotify_account(interaction: discord.Interaction):
#     pass