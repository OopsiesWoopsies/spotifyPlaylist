from spotify_util_functions import get_token, util

from requests import get
from urllib.parse import quote
import json


def encode_url(query: str) -> str:
    return quote(query)


def search_for_artist(token: str, artist_name: str) -> dict:
    limit = 5
    url = util.SPOTIFY_API_URL + f"/search?q={encode_url(artist_name)}&type=artist&limit={limit}"
    headers = get_token.get_auth_headers(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    return json_result


def get_songs(token: str, artist_id: str) -> dict:
    url = util.SPOTIFY_API_URL + f"/artists/{encode_url(artist_id)}/top-tracks?country=CA"
    headers = get_token.get_auth_headers(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]

    return json_result


def get_playlist(token: str, keyword: str, offset: str = "0") -> dict:
    url = util.SPOTIFY_API_URL + f"/search?q={encode_url(keyword)}&type=playlist&limit=50&offset={offset}"
    headers = get_token.get_auth_headers(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    return json_result["playlists"]