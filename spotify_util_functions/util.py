import json

from spotify_util_functions import get_token
from requests import get


SPOTIFY_API_URL = "https://api.spotify.com/v1"


def get_json_from_href(token: str, href: str) -> dict:
    """
    Sends a request to Spotify api to retrieve information from the href provided.
    :param token: A Spotify access token.
    :param href: A URL.
    :return: A json formatted dictionary.
    """

    headers = get_token.get_auth_headers(token)
    result = get(href, headers=headers)
    json_result = json.loads(result.content)

    return json_result


def get_page(token: str, json_result_items: dict, page: str) -> dict:
    """
    Sends a request to Spotify api to retrieve information regarding the next or previous page of the given json result.
    :param token: A Spotify access token.
    :param json_result_items: A json formatted dictionary of items.
    :param page: "Next" or "Previous" to indicate forward or back.
    :return: A json formatted dictionary of the next or previous page.
    """

    if json_result_items[page] is None:
        return {"error": {
            "message": f"No {page} href"
            }
        }

    return get_json_from_href(token, json_result_items[page])