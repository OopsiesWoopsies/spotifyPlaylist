import json
from requests import get, post

from util_functions import get_token


def get_playlists(token: str) -> dict:
    url = "https://api.spotify.com/v1/me/playlists"
    header = get_token.get_auth_headers(token)

    result = get(url, headers=header)
    json_result = json.loads(result.content)
    return json_result["items"]


def create_playlist(token: str, playlist_name: str = "New Playlist", description: str = "", public: bool = False) -> dict:
    url = f"https://api.spotify.com/v1/me/playlists"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
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
    url = href
    headers = get_token.get_auth_headers(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    return json_result

def add_songs_to_playlist(): # Unsure of parameters yet
    pass
