from spotify_util_functions import get_token, playlist_functions

import util


def playlist_things(local_token: str, local_expiry: float):
    while True:
        util.print_choices(util.playlist_options)
        choice = input("Enter #: ")

        token, expiry = get_token.check_expiration(local_token, local_expiry)

        if choice == "1": # View playlists
            if (json_result := check_json_size(token))["total"] == 0:
                continue

            choice = util.choice_validation(f"View playlist's tracks (1-{json_result["total"]}): ", json_result["total"]) # Consider the page turning for playlists and many other things
            playlist_choice = json_result["items"][choice-1]
            token, expiry = get_token.check_expiration(token, expiry)

            print("\nTracks in " + playlist_choice["name"])
            json_result = playlist_functions.get_playlist_tracks(token, playlist_choice["tracks"]["href"])

            if json_result["total"] == 0:
                print(f"Wait a minute... there's no tracks in {playlist_choice["name"]}!\n")
                continue

            for i in range(len(json_result["items"])):
                print(f"{i+1}. {json_result["items"][i]["track"]["name"]}")

            util.view_with_pages(token, json_result)

        elif choice == "2": # Playlist creation
            playlist_name = input("Enter a name for the new playlist: ")
            description = input("Enter a description: ")
            token, expiry = get_token.check_expiration(token, expiry)

            if playlist_name == "":
                playlist_name = "New Playlist"

            playlist_functions.create_playlist(token, playlist_name, description)

        elif choice == "3": # Playlist generator
            keyword = input("Enter a keyword: ") # Test symbols
            amount = util.choice_validation("Amount of songs (30-100): ", 100, 30)
            token, expiry = get_token.check_expiration(token, expiry)

            playlist_functions.generate_playlist(token, keyword, amount)
            print("Playlist created")

        elif choice == "4": # Removing playlist
            if (json_result := check_json_size(token))["total"] == 0:
                continue

            choice = util.choice_validation(f"Remove a playlist from your library (1-{json_result["total"]}): ",json_result["total"])
            playlist_choice = json_result["items"][choice - 1]

            print("1. Yes\n2. No\n")
            choice = util.choice_validation(f"Are you SURE you want to remove {playlist_choice["name"]} from your library (this action cannot be undone)? (1-2): ", 2)
            token, expiry = get_token.check_expiration(token, expiry)

            if choice == 1:
                playlist_functions.remove_playlist_from_library(token, playlist_choice["id"])
                print("Consider it... GONE!!!")
            else:
                print("Close one...")

        elif choice == "5":  # Edit playlist
            if (json_result := check_json_size(token))["total"] == 0:
                continue

            choice = util.choice_validation(f"Pick a playlist to edit its information (1-{json_result["total"]}): ", json_result["total"])
            playlist_choice = json_result["items"][choice - 1]

            edit_playlist(token, expiry, playlist_choice["id"])

        elif choice == str(len(util.playlist_options)): # Exit
            break

        print()


def edit_playlist(local_token: str, local_expiry: float, playlist_id: str):
    field_change_options = ["name", "description"]

    while True:
        util.print_choices(util.edit_playlist_options)
        choice = input("Enter #: ")

        if choice == "1" or choice == "2":
            new_field_change = input(f"New {field_change_options[int(choice)-1]} for this playlist: ")

            token, expiry = get_token.check_expiration(local_token, local_expiry)
            playlist_functions.edit_playlist(token, playlist_id, field_change_options[int(choice)-1], new_field_change)

        if choice == str(len(util.edit_playlist_options)):
            return

        else:
            print("Invalid #")

def check_json_size(token: str) -> dict:
    json_result = playlist_functions.get_playlists(token)

    if json_result["total"] == 0:
        print("No playlists! Create one first!")
        return json_result

    json_result = json_result

    for i, val in enumerate(json_result["items"]):
        print(f"{i + 1}. {val["name"]}")

    return json_result