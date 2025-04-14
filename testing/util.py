choices = ["Current User Options", "Artists", "Quit"]
user_options = ["Current User", "User Top Artists", "User Top Tracks", "Playlist Options", "Go Back"]
playlist_options = ["Get Playlists & Tracks", "Create Playlist", "Edit Playlist Information", "Update Playlist", "Go Back"] # Make it so you can view everything in a playlist since the limit is 50

edit_playlist = ["Change Name", "Change Description", "Toggle Publication", "Toggle Collaborate", "Go Back"]
update_playlist = ["Add a Song", "Remove a Song", "Go Back"]


time_range_choices = ["~4 weeks", "~6 months", "~1 year"]
page_options = ["Previous", "Next", "Back"]

# ----------------------------------------------------------------------------------------------------------------------

def print_choices(arr: list):
    for i, val in enumerate(arr):
        print(f"{i+1}. {val}")

    print()


def choice_validation(message: str, cap: int) -> str:
    while True:
        choice = input(message)
        if choice.isdigit() and 0 < int(choice) <= cap:
            return choice
        else:
            print("Invalid #.")
