from spotify_util_functions import get_token, searching

import util, user_tests

if __name__ == "__main__":
    token, expiry = get_token.get_token(get_token.test_refresh_token)

    if token is None:
        print("Token is cooked! Something went wrong.")
        exit()
    while True:
        util.print_choices(util.choices)
        choice = input("Enter #: ")
        print()

        token, expiry = get_token.check_expiration(token, get_token.test_refresh_token, expiry)

        if choice == "1":                                       # User related options
            user_tests.user_things(token, get_token.test_refresh_token, expiry)

        elif choice == "2":
            while True:
                artist_name = input("Enter artist name: ")
                if len(artist_name) > 0:
                    print()
                    break
                print("Not a valid name.\n")

            token, expiry = get_token.check_expiration(token, get_token.test_refresh_token, expiry)

            json_result = searching.search_for_artist(token, artist_name)
            if json_result is not None and "error" not in json_result:
                for i, val in enumerate(json_result):
                    print(f"{str(i+1) + '. ' + val["name"]:<30s} Popularity: {str(val["popularity"]) + '/100':<50s}")

                artist_id_num = util.choice_validation("Artist #: ", len(json_result))
                artist_id = json_result[artist_id_num-1]["id"]

                print(f"\nShowing results for {json_result[artist_id_num-1]["name"]}: \nPopularity: {json_result[artist_id_num-1]["popularity"]}/100\n")
                json_result = searching.get_songs(token, artist_id)

                for i, val in enumerate(json_result):
                    print(f"{str(i+1) + '. ' + val["name"]:<100s} Popularity: {str(val["popularity"]) + '/100':<10s}")
                    print("-"*130)
                print()
        elif choice == str(len(util.choices)):
            break
        else:
            print("Not valid.\n")
