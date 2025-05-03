from spotify_util_functions import get_token, user_functions

import discord
from discord import app_commands


spotify_token, spotify_expiry = get_token.get_token() # change this to get user specific token using dictionary
GUILD_ID = discord.Object(id=1366142338342322397)

def setup(bot):
    @bot.tree.command(name="user", description="User related commands", guild=GUILD_ID)
    @app_commands.choices(user=[
        app_commands.Choice(name='current-user', value='current_user'),
        app_commands.Choice(name='authorize', value='authorize'),
    ])
    async def user(interaction: discord.Interaction, user: app_commands.Choice[str]):
        global spotify_expiry, spotify_token
        user_id = interaction.user.id  # check if id is in env file before printing (same for every user related slash command)
        print(user_id)

        if user.value == "current_user":
            await interaction.response.send_message(user_functions.get_current_user(spotify_token), ephemeral=True)

        if user.value == "authorize":
            print("authorizing")
            # spotify_token, spotify_expiry =