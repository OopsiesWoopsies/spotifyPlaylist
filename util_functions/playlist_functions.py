import json
from requests import get, post

from util_functions import get_token, util


def get_playlists(token: str) -> dict:
    url = "https://api.spotify.com/v1/me/playlists"
    header = get_token.get_auth_headers(token)

    result = get(url, headers=header)
    json_result = json.loads(result.content)

    return json_result["items"]


def create_playlist(token: str, playlist_name: str = "New Playlist", description: str = "", public: bool = False) -> dict:
    url = "https://api.spotify.com/v1/me/playlists"
    headers = get_token.get_auth_headers(token)
    data = {
        "name": playlist_name,
        "description": description,
        "public": public
    }

    data = json.dumps(data)
    result = post(url, data=data, headers=headers)
    json_result = json.loads(result.content)

    return json_result


def get_playlist_tracks(token, href: str) -> dict:
    return util.get_json_from_href(token, href)

def auto_add_songs_to_new_playlist(token: str) -> None: # Unsure of parameters yet
    pass # use playlist searching

def manual_add_songs_to_playlist(token: str, playlist: str, song: str) -> None: # Gonna be empty for a while (not sure if feature)
    pass