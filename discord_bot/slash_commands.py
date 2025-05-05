from spotify_util_functions import get_token, user_functions
from utils.user_tokens import spotify_tokens

import discord
from discord import app_commands

import os


GUILD_ID = discord.Object(id=os.getenv("DISCORD_SERVER_ID"))

def setup(bot):
    def check_spotify_token(user_id: str, token: str, refresh_token: str, expiration: int) -> tuple:
        new_token, spotify_token_expiration = get_token.check_expiration(token, refresh_token, expiration)

        if token != new_token:
            token = new_token
            spotify_tokens["users"][user_id]["spotify_token"] = token

        # Consider updating json file ALSO FIX TESTING FILES FROM UPDATED PARAMETERS

        return token, expiration


    @bot.tree.command(name="user", description="User related commands", guild=GUILD_ID)
    @app_commands.choices(user=[
        app_commands.Choice(name='current-user', value='current_user'),
        app_commands.Choice(name='authorize', value='authorize'),
    ])
    async def user(interaction: discord.Interaction, user: app_commands.Choice[str]):
        user_id = str(interaction.user.id)
        print(user_id)
        if user_id in spotify_tokens["users"]:
            spotify_token_info = spotify_tokens["users"][user_id]
            spotify_token = spotify_token_info["spotify_token"]
            spotify_refresh_token = spotify_token_info["spotify_refresh_token"]
            spotify_token_expiration = spotify_token_info["expiration_time"]

            spotify_token, spotify_token_expiration = check_spotify_token(user_id, spotify_token, spotify_refresh_token, spotify_token_expiration)

            print(spotify_token)

            if user.value == "current_user":
                await interaction.response.send_message(user_functions.get_current_user(spotify_token), ephemeral=True)
        else:
            await interaction.response.send_message("Authorize first with user authorize!", ephemeral=True)

        if user.value == "authorize":
            print("authorizing")
            # unfinished