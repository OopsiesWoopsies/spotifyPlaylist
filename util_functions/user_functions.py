from util_functions import get_token, util

from requests import get
import json


def get_current_user(token: str):
    url = util.SPOTIFY_API_URL + "/me"
    headers = get_token.get_auth_headers(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    return json_result


def get_top_user_artists(token: str, limit: str, time_range: str) -> dict:
    time = ["short_term", "medium_term", "long_term"]  # long_term --> ~ 1 year | medium_term --> ~ 6 months | short_term ~ 4 weeks
    offset = 0
    url = util.SPOTIFY_API_URL + f"/me/top/artists?time_range={time[(int(time_range)-1)]}&limit={limit}&offset={offset}"
    headers = get_token.get_auth_headers(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    return json_result["items"]


def get_top_user_tracks(token: str, limit: str, time_range: str) -> dict:
    time = ["short_term", "medium_term", "long_term"] # long_term --> ~ 1 year | medium_term --> ~ 6 months | short_term ~ 4 weeks
    offset = 0
    url = util.SPOTIFY_API_URL + f"/me/top/tracks?time_range={time[(int(time_range)-1)]}&limit={limit}&offset={offset}"
    headers = get_token.get_auth_headers(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)

    return json_result["items"]