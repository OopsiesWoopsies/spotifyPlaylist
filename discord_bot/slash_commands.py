from spotify_util_functions import get_token, user_functions
from utils.user_tokens import spotify_tokens

import discord
from discord import app_commands


# spotify_token, spotify_expiry = get_token.get_token() # change this to get user specific token using dictionary
GUILD_ID = discord.Object(id=1366142338342322397)

def setup(bot):
    @bot.tree.command(name="user", description="User related commands", guild=GUILD_ID)
    @app_commands.choices(user=[
        app_commands.Choice(name='current-user', value='current_user'),
        app_commands.Choice(name='authorize', value='authorize'),
    ])
    async def user(interaction: discord.Interaction, user: app_commands.Choice[str]):
        user_id = str(interaction.user.id)

        print(user_id)
        if user_id in spotify_tokens["users"]: # put spotify token in json as well as expiration date in get_token()
            if user.value == "current_user":
                await interaction.response.send_message(user_functions.get_current_user(spotify_tokens["users"][user_id][""]), ephemeral=True)
        else:
            await interaction.response.send_message("Authorize first with user authorize!", ephemeral=True)

        if user.value == "authorize":
            print("authorizing")
            # spotify_token, spotify_expiry =