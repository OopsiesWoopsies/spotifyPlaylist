import util_functions

choices = ["Current User Options", "Artists", "Quit"]
user_options = ["Current User", "User Top Artists", "User Top Tracks", "Playlist Options", "Go Back"]
playlist_options = ["Get Playlists & Tracks", "Create Playlist", "Auto-Playlist", "Remove Playlist", "Edit Playlist Information", "Go Back"]

edit_playlist_options = ["Change Name", "Change Description", "Go Back"]

time_range_choices = ["~4 weeks", "~6 months", "~1 year"]
page_options = ["Next", "Previous", "Back"]


# ----------------------------------------------------------------------------------------------------------------------


def print_choices(arr: list) -> None:
    for i, val in enumerate(arr):
        print(f"{i+1}. {val}")
    print()


def choice_validation(message: str, cap: int, minimum: int = 1) -> int:
    while True:
        choice = input(message)
        if choice.isdigit() and minimum <= int(choice) <= cap:
            return int(choice)
        else:
            print("Invalid #.")


def view_with_pages(token: str, json_result: dict) -> None:
    while True:
        print_choices(page_options)
        choice = choice_validation(f"(1-3): ", 3)
        print()

        if choice == 3:
            return

        if choice == 1:
             check_result = util_functions.util.get_page(token, json_result, "next")
             if "error" not in check_result:
                 json_result = check_result

        elif choice == 2:
            check_result = util_functions.util.get_page(token, json_result, "previous")
            if "error" not in check_result:
                json_result = check_result

        for i in range(len(json_result["items"])):
            print(f"{i+1}. {json_result["items"][i]["track"]["name"]}")