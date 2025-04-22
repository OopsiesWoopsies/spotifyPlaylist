from util_functions import get_token, playlist_functions

import util


def playlist_things(local_token, local_expiry):
    while True:
        util.print_choices(util.playlist_options)
        choice = input("Enter #: ")

        token, expiry = get_token.check_expiration(local_token, local_expiry)

        if choice == "1": # View playlists
            json_result = playlist_functions.get_playlists(token)
            size = json_result["total"]

            if size == 0:
                print("No playlists! Create one first!")
                continue

            json_result = json_result["items"]

            for i, val in enumerate(json_result):
                print(f"{i+1}. {val["name"]}")

            choice = util.choice_validation(f"View playlist's tracks (1-{size}): ", size) # Consider the page turning for playlists and many other things
            playlist_choice = json_result[choice-1]

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

            if playlist_name == "":
                playlist_name = "New Playlist"

            playlist_functions.create_playlist(token, playlist_name, description)

        elif choice == "3": # Playlist generator
            keyword = input("Enter a keyword: ") # Test symbols
            amount = util.choice_validation("Amount of songs (30-100): ", 100, 30)
            playlist_functions.generate_playlist(token, keyword, amount)
            print("Playlist created")

        elif choice == "4": # Removing playlist
            json_result = playlist_functions.get_playlists(token)
            size = json_result["total"]

            if size == 0:
                print("No playlists! Create one first!")
                continue

            json_result = json_result["items"]

            for i, val in enumerate(json_result):
                print(f"{i + 1}. {val["name"]}")

            choice = util.choice_validation(f"Remove a playlist from your library (1-{size}): ",size)
            playlist_choice = json_result[choice - 1]

            print("1. Yes\n2. No\n")
            choice = util.choice_validation(f"Are you SURE you want to remove {playlist_choice["name"]} from your library (this action cannot be undone)? (1-2): ", 2)
            if choice == 1:
                playlist_functions.remove_playlist_from_library(token, playlist_choice["id"])
                print("Consider it... GONE!!!")
            else:
                print("Close one...")

        elif choice == "5":  # Edit playlist
            pass

        elif choice == str(len(util.playlist_options)): # Exit
            break

        print()