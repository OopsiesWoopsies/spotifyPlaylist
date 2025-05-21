from spotify_util_functions import get_token, util

from requests import get
import json


def get_current_user(token: str) -> dict:
    """
    Sends a request to Spotify api to retrieve information about the current user.
    :param token: A Spotify access token.
    :return: A json formatted dictionary.
    """

    url = util.SPOTIFY_API_URL + "/me"
    headers = get_token.get_auth_headers(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    return json_result


def get_top_user_artists(token: str, limit: str, time_range: str) -> dict:
    """
    Sends a request to Spotify api to retrieve information about the current user's top artists from between a month to a year.
    :param token: A Spotify access token.
    :param limit: The amount of results to return. Must be between 1 and 50 inclusive.
    :param time_range: A number between 1-3 inclusive as a string. Short term to long term.
    :return: A json formatted dictionary of items.
    """

    time = ["short_term", "medium_term", "long_term"]  # long_term --> ~ 1 year | medium_term --> ~ 6 months | short_term ~ 4 weeks
    offset = 0
    url = util.SPOTIFY_API_URL + f"/me/top/artists?time_range={time[(int(time_range)-1)]}&limit={limit}&offset={offset}"
    headers = get_token.get_auth_headers(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    return json_result["items"]


def get_top_user_tracks(token: str, limit: str, time_range: str) -> dict:
    """
    Sends a request to Spotify api to retrieve information about the current user's top tracks from between a month to a year.
    :param token: A Spotify access token.
    :param limit: The amount of results to return. Must be between 1 and 50 inclusive.
    :param time_range: A number between 1-3 inclusive as a string. Short term to long term.
    :return: A json formatted dictionary of items.
    """

    time = ["short_term", "medium_term", "long_term"] # long_term --> ~ 1 year | medium_term --> ~ 6 months | short_term ~ 4 weeks
    offset = 0
    url = util.SPOTIFY_API_URL + f"/me/top/tracks?time_range={time[(int(time_range)-1)]}&limit={limit}&offset={offset}"
    headers = get_token.get_auth_headers(token)

    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    return json_result["items"]