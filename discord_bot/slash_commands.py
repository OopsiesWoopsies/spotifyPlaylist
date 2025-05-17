from spotify_util_functions import get_token, user_functions, playlist_functions, util
from utils.user_tokens import spotify_tokens
from utils import user_tokens

import discord
from discord import app_commands

import os
import asyncio


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


    @bot.tree.command(name="generate_playlist", description="Generate a random playlist", guild=GUILD_ID)
    async def playlist_generation(interaction: discord.Interaction, keyword: str, song_amount: int = 30):
        user_id = str(interaction.user.id)
        spotify_token = check_user_authorized(user_id)
        if not spotify_token:
            await interaction.response.send_message("Authorize first with user authorize!", ephemeral=True)
            return

        if song_amount < 30:
            song_amount = 30
        if song_amount > 100:
            song_amount = 100

        await interaction.response.send_message(f"Generating a playlist with {song_amount} songs and {keyword}...", ephemeral=True)
        playlist_functions.generate_playlist(spotify_token,keyword, song_amount)
        message = await interaction.original_response()
        await message.edit(content="Playlist generated! Check your spotify!")


    @bot.tree.command(name="delete_playlist", description="Delete a playlist from your library", guild=GUILD_ID)
    async def delete_playlist(interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        spotify_token = check_user_authorized(user_id)
        if not spotify_token:
            await interaction.response.send_message("Authorize first with user authorize!", ephemeral=True)
            return


        def check(reaction, user):
            return user == interaction.user and str(reaction.emoji) in ["⬅️", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "➡️"] and reaction.message.id == message.id


        def get_playlist_names(json_result: dict) -> str:
            names = ""
            for i, val in enumerate(json_result):
                names += f"{i+1}. " + val["name"] + "\n"

            return names


        async def remove_playlist(playlist_id: str, playlist_name: str) -> None:
            nonlocal message
            playlist_functions.remove_playlist_from_library(spotify_token, playlist_id)
            await message.edit(content=f"Removed {playlist_name} from your library")


        number_emojis = {
            1: "1️⃣",
            2: "2️⃣",
            3: "3️⃣",
            4: "4️⃣",
            5: "5️⃣"
        }
        user_spotify_playlists = playlist_functions.get_playlists(spotify_token, limit=5)
        next_href = user_spotify_playlists["next"]
        pages = [user_spotify_playlists["items"]]

        current_page = 0
        await interaction.response.send_message(get_playlist_names(pages[current_page]))
        followup = await interaction.followup.send("Pick a playlist to remove from your library (there are no confirmations, beware).")

        message = await interaction.original_response()
        await message.add_reaction("⬅️")
        for num in range(len(user_spotify_playlists["items"])):
            await message.add_reaction(number_emojis[num+1])
        await message.add_reaction("➡️")

        while True:
            try:
                reaction, _ = await bot.wait_for("reaction_add", timeout=30.0, check=check)

                if str(reaction.emoji) == "➡️" and (next_href is not None or current_page < len(pages)-1):
                    current_page += 1
                    if current_page > len(pages)-1 and next_href is not None:
                        next_page_playlists = util.get_json_from_href(spotify_token, next_href)
                        pages.append(next_page_playlists["items"])
                        next_href = next_page_playlists["next"]

                elif str(reaction.emoji) == "⬅️" and current_page > 0:
                    current_page -= 1

                await message.edit(content=get_playlist_names(pages[current_page]))

                if str(reaction.emoji) == "5️⃣" and len(pages[current_page]) == 5:
                    await remove_playlist(pages[current_page][4]["id"], pages[current_page][4]["name"])
                    break

                elif str(reaction.emoji) == "4️⃣" and len(pages[current_page]) >= 4:
                    await remove_playlist(pages[current_page][3]["id"], pages[current_page][3]["name"])
                    break

                elif str(reaction.emoji) == "3️⃣" and len(pages[current_page]) >= 3:
                    await remove_playlist(pages[current_page][2]["id"], pages[current_page][2]["name"])
                    break

                elif str(reaction.emoji) == "2️⃣" and len(pages[current_page]) >= 2:
                    await remove_playlist(pages[current_page][1]["id"], pages[current_page][1]["name"])
                    break

                elif str(reaction.emoji) == "1️⃣" and len(pages[current_page]) >= 1:
                    await remove_playlist(pages[current_page][0]["id"], pages[current_page][0]["name"])
                    break

                await message.remove_reaction(reaction.emoji, interaction.user)

            except asyncio.TimeoutError:
                break
        await message.clear_reactions()
        await followup.delete()


# ------------------------------------------------------------------------------------------------------------


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

        if user.value == "current_user":  # Format this later
            json_result = user_functions.get_current_user(spotify_token)
            await interaction.response.send_message(f"Hey {json_result["display_name"]}!\n\nThat's you... right?", ephemeral=True)

        elif user.value == "authorize" and user_id not in spotify_tokens["users"]:
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


    @bot.tree.command(name="tops", description="Get your top tracks / artists!", guild=GUILD_ID)
    @app_commands.choices(top_choice=[
        app_commands.Choice(name="top_tracks", value="track"),
        app_commands.Choice(name="top_artists", value="artist")
    ])
    @app_commands.choices(time_range=[
        app_commands.Choice(name="1y", value="3"),
        app_commands.Choice(name="6m", value="2"),
        app_commands.Choice(name="4w", value="1")
    ])
    async def top_items(interaction: discord.Interaction, top_choice: app_commands.Choice[str], time_range: app_commands.Choice[str], amount: int = 5):
        user_id = str(interaction.user.id)
        spotify_token = check_user_authorized(user_id)
        json_result = None
        if not spotify_token:
            await interaction.response.send_message("Authorize first with user authorize!", ephemeral=True)
            return


        def get_artists(json_artists_result: dict) -> str:
            artist_names = ""
            for val in range(len(json_artists_result)-1):
                artist_names += json_artists_result[val]["name"] + ", "

            artist_names += json_artists_result[len(json_artists_result)-1]["name"]

            return artist_names


        if amount < 1:
            amount = 1
        if amount > 10:
            amount = 10

        if top_choice.value == "track":
            json_result = user_functions.get_top_user_tracks(spotify_token, str(amount), time_range.value)

        if top_choice.value == "artist":
            json_result = user_functions.get_top_user_artists(spotify_token, str(amount), time_range.value)

        build_string = ""
        for i, val in enumerate(json_result):
            build_string += f"{i+1}. {val["name"]}\nPopularity: {str(val["popularity"]) + '/100'}"
            if top_choice.value == "track":
                build_string += f"\nArtist: {get_artists(val["artists"])}"
            elif top_choice.value == "artist":
                build_string += f"\nFollowers: {val["followers"]["total"]:,}"

            build_string += "\n\n"

        await interaction.response.send_message(f"```Here are your top {top_choice.value}s!\n\n{build_string}```", ephemeral=True)