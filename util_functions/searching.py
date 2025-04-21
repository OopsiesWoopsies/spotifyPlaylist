from util_functions import get_token, util

from requests import get
import json


def search_for_artist(token: str, artist_name: str) -> dict:
    limit = 5
    url = f"https://api.spotify.com/v1/search?q={artist_name}&type=artist&limit={limit}"
    headers = get_token.get_auth_headers(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    return json_result

def get_songs(token: str, artist_id: str) -> dict:
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=CA"
    headers = get_token.get_auth_headers(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]

    return json_result

def get_playlist(token: str, keyword: str, offset: str = "0") -> dict:
    url = f"https://api.spotify.com/v1/search?q={keyword}&type=playlist&limit=50&offset={offset}"
    headers = get_token.get_auth_headers(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    return json_result["playlists"]