import json

# Loads the .json file
try:
    with open("../user.json", mode="r") as f:
        spotify_tokens = json.load(f)
except Exception as e:
    print(f"Something went wrong: {e}")
    exit(-1)


def write_json() -> None:
    """
    Writes to the .json file, saving all the user data (user tokens and the such).
    :return: None.
    """

    try:
        with open("../user.json", mode="w") as f:
            json.dump(spotify_tokens, f, indent=2)
    except Exception as e:
        print(f"Something went wrong: {e}")