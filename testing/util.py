import spotify_util_functions

choices = ["Current User Options", "Artists", "Quit"]
user_options = ["Current User", "User Top Artists", "User Top Tracks", "Playlist Options", "Go Back"]
playlist_options = ["Get Playlists & Tracks", "Create Playlist", "Auto-Playlist", "Remove Playlist", "Edit Playlist Information", "Go Back"]

edit_playlist_options = ["Change Name", "Change Description", "Go Back"]

time_range_choices = ["~4 weeks", "~6 months", "~1 year"]
page_options = ["Next", "Previous", "Back"]


# ----------------------------------------------------------------------------------------------------------------------


def print_choices(arr: list) -> None:
    """
    Prints a given list in the format of a numbered list.
    :param arr: The list to print out in a numbered list format.
    :return: None.
    """

    for i, val in enumerate(arr):
        print(f"{i+1}. {val}")
    print()


def choice_validation(message: str, cap: int, minimum: int = 1) -> int:
    """
    Ensures a valid input from the user.
    :param message: Message to print.
    :param cap: The maximum threshold for validity.
    :param minimum: The minimum threshold for validity. Default: 1.
    :return: The choice as an integer.
    """

    while True:
        choice = input(message)
        if choice.isdigit() and minimum <= int(choice) <= cap:
            return int(choice)
        else:
            print("Invalid #.")


def view_with_pages(token: str, json_result: dict) -> None:
    """
    Enables the user to go back and forth to the next or previous json results to view them in the terminal.
    :param token: Spotify access token.
    :param json_result: The first json result that leads to the next.
    :return: None.
    """

    while True:
        print_choices(page_options)
        choice = choice_validation(f"(1-3): ", 3)
        print()

        if choice == 3: # Exit case
            return

        # Grabs the next page
        if choice == 1:
             check_result = spotify_util_functions.util.get_page(token, json_result, "next")
             if "error" not in check_result:
                 json_result = check_result

        # Grabs the previous page
        elif choice == 2:
            check_result = spotify_util_functions.util.get_page(token, json_result, "previous")
            if "error" not in check_result:
                json_result = check_result

        # Prints out tracks in a list format
        for i in range(len(json_result["items"])):
            print(f"{i+1}. {json_result["items"][i]["track"]["name"]}")