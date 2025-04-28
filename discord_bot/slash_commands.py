from spotify_util_functions import get_token, user_functions

import discord
from discord.ext import commands

spotify_token, spotify_expiry = get_token.get_token()


def setup(bot: commands.Bot, GUILD_ID) -> None:
    @bot.tree.command(name="amigo", description="Say hola", guild=GUILD_ID)
    async def hello(interaction: discord.Interaction):

        await interaction.response.send_message(user_functions.get_current_user(spotify_token),ephemeral=True)

