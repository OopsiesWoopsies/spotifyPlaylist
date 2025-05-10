from spotify_util_functions import get_token, user_functions
from utils.user_tokens import spotify_tokens
from utils import user_tokens

import discord
from discord import app_commands

import os


GUILD_ID = discord.Object(id=os.getenv("DISCORD_SERVER_ID"))

def setup(bot):
    def check_user_authorized(user_id: str) -> str | None:
        if user_id in spotify_tokens["users"]:
            spotify_token_info = spotify_tokens["users"][user_id]
            spotify_token = spotify_token_info["spotify_token"]
            spotify_refresh_token = spotify_token_info["spotify_refresh_token"]
            spotify_token_expiration = spotify_token_info["expiration_time"]
            new_token, spotify_token_expiration = get_token.check_expiration(spotify_token, spotify_refresh_token, spotify_token_expiration)

            if spotify_token != new_token:
                spotify_token = new_token
                spotify_tokens["users"][user_id]["spotify_token"] = spotify_token
                spotify_tokens["users"][user_id]["expiration_time"] = spotify_token_expiration

            return spotify_token


    @bot.tree.command(name="user", description="User related commands", guild=GUILD_ID)
    @app_commands.choices(user=[
        app_commands.Choice(name='current-user', value='current_user'),
        app_commands.Choice(name='authorize', value='authorize'),
    ])
    async def user(interaction: discord.Interaction, user: app_commands.Choice[str]):
        user_id = str(interaction.user.id)
        spotify_token = check_user_authorized(user_id)
        if user.value != "authorize" and not spotify_token:
            await interaction.response.send_message("Authorize first with user authorize!", ephemeral=True)
            return

        if user.value == "current_user": # Format this later
            await interaction.response.send_message(user_functions.get_current_user(spotify_token), ephemeral=True)

        if user.value == "authorize" and user_id not in spotify_tokens["users"]:
            await interaction.response.send_message("Authorizing...", ephemeral=True)
            spotify_refresh_token, spotify_token, spotify_token_expiration = await get_token.get_refresh_token()

            spotify_tokens["users"][user_id] = {
                "spotify_token": spotify_token,
                "spotify_refresh_token": spotify_refresh_token,
                "expiration_time": spotify_token_expiration
            }
            user_tokens.write_json()
            await interaction.followup.send("Authorized!", ephemeral=True)

        else:
            await interaction.response.send_message("Already authorized!", ephemeral=True)


    @bot.tree.command(name="generate_playlist", description="Generate a random playlist", guild=GUILD_ID)
    async def playlist_generation(interaction: discord.Interaction, keyword: str, number_of_songs: int = 30):
        user_id = str(interaction.user.id)
        spotify_token = check_user_authorized(user_id)
        if not spotify_token:
            await interaction.response.send_message("Authorize first with user authorize!", ephemeral=True)
            return

