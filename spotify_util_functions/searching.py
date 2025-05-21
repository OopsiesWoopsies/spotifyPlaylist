from spotify_util_functions import get_token, util

from requests import get
from urllib.parse import quote
import json


def encode_url(query: str) -> str:
    """
    Encodes a string into a valid query to be used in an HTTP request.
    :param query: A string query.
    :return: An encoded valid query.
    """

    return quote(query)


def search_for_artist(token: str, artist_name: str) -> dict:
    """
    Sends a request to Spotify api to retrieve the artist results.
    :param token: A Spotify access token.
    :param artist_name: Artist name.
    :return: A json formatted dictionary of artists and their information.
    """

    limit = 5
    url = util.SPOTIFY_API_URL + f"/search?q={encode_url(artist_name)}&type=artist&limit={limit}"
    headers = get_token.get_auth_headers(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]

    return json_result


def get_songs(token: str, artist_id: str) -> dict:
    """
    Sends a request to Spotify api to retrieve information about an artist's top tracks.
    :param token: A Spotify access token.
    :param artist_id: An artist's Spotify id.
    :return: A json formatted dictionary of the artist's top tracks.
    """

    url = util.SPOTIFY_API_URL + f"/artists/{encode_url(artist_id)}/top-tracks?country=CA"
    headers = get_token.get_auth_headers(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]

    return json_result


def get_playlist(token: str, keyword: str, offset: str = "0") -> dict:
    """
    Sends a request to Spotify api to retrieve the search results from the given keyword.
    :param token: A Spotify access token.
    :param keyword: The search keyword.
    :param offset: The index of the first result to return. Default: "0".
    :return: A json formatted dictionary of the search results.
    """

    url = util.SPOTIFY_API_URL + f"/search?q={encode_url(keyword)}&type=playlist&limit=50&offset={offset}"
    headers = get_token.get_auth_headers(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    return json_result["playlists"]