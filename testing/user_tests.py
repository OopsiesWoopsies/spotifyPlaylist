from spotify_util_functions import get_token, user_functions

import util, playlist_tests


def user_things(local_token: str, refresh_token: str, local_expiry: float) -> None:
    """
    Testing user functions.
    :param local_token: Spotify access token.
    :param refresh_token: Spotify refresh token.
    :param local_expiry: Expiry time for the access token.
    :return: None.
    """

    while True:
        util.print_choices(util.user_options)
        choice = input("Enter #: ")
        print()

        token, expiry = get_token.check_expiration(local_token, refresh_token, local_expiry)

        if choice == "1": # User info
            json_result = user_functions.get_current_user(token)
            print(json_result) # Unformatted

        elif choice == "2": # Top artists
            limit = util.choice_validation("Enter # of tracks (1-50): ", 50)
            print()

            util.print_choices(util.time_range_choices)
            time_range = util.choice_validation("Top artists from: (1-3): ", 3)
            print()
            json_result = user_functions.get_top_user_artists(token, str(limit), str(time_range))
            # Prints out the user's top artists with their information in a numbered list format.
            for i, val in enumerate(json_result):
                print(f"{str(i+1) + '. ' + val["name"]:<40} Genre(s): {str(val["genres"]):<100} Popularity: {str(val["popularity"]) + '/100':<10} Followers: {val["followers"]["total"]:<20,}")
                print("-" * 200)

        elif choice == "3": # Top tracks
            limit = util.choice_validation("Enter # of tracks (1-50): ", 50)
            print()

            util.print_choices(util.time_range_choices)
            time_range = util.choice_validation("Top artists from: (1-3): ", 3)
            print()

            json_result = user_functions.get_top_user_tracks(token, str(limit), str(time_range))
            # Prints out the user's top tracks with their information in a numbered list format.
            for i, val in enumerate(json_result):
                print(f"{str(i+1) + '. ' + val["name"]:<70} Popularity: {str(val["popularity"]) + '/100':<10} Artist: {val["artists"][0]["name"]:<10}")
                print("-" * 150)

        elif choice == "4": # Playlist options
            playlist_tests.playlist_things(token, refresh_token, expiry)

        elif choice == str(len(util.user_options)):
            return
        else:
            print("Not valid.\n")

        print()