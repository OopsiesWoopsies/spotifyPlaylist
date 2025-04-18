from util_functions import get_token, playlist_functions

import util

def playlist_things(local_token, local_expiry):
    while True:
        util.print_choices(util.playlist_options)
        choice = input("Enter #: ")

        token, expiry = get_token.check_expiration(local_token, local_expiry)

        if choice == "1":
            json_result = playlist_functions.get_playlists(token)
            size = len(json_result)

            if size == 0:
                print("No playlists! Create one first!")
                continue

            for i, val in enumerate(json_result):
                print(f"{i+1}. {val["name"]}")

            choice = util.choice_validation(f"View playlist's tracks (1-{size}): ", size) # Consider the page turning for playlists
            playlist_choice = json_result[choice-1]

            print("\nTracks in " + playlist_choice["name"])
            json_result = playlist_functions.get_playlist_tracks(token, playlist_choice["tracks"]["href"])

            print(json_result)

            if len(json_result["items"]) == 0:
                print(f"Wait a minute... there's no tracks in {playlist_choice["name"]}!\n")
                continue

            for i in range(len(json_result["items"])):
                print(f"{i+1}. {json_result["items"][i]["track"]["name"]}")

            util.view_with_pages(token, json_result)

        elif choice == "2":
            playlist_name = input("Enter a name for the new playlist: ")
            description = input("Enter a description: ")

            if playlist_name == "":
                playlist_name = "New Playlist"

            json_result = playlist_functions.create_playlist(token, playlist_name, description)

        elif choice == "3":
            pass

        elif choice == "4":
            pass

        elif choice == str(len(util.playlist_options)):
            break

        print()