import json

from util_functions import get_token
from requests import get


def get_json_from_href(token: str, href: str) -> dict:
    headers = get_token.get_auth_headers(token)
    result = get(href, headers=headers)
    json_result = json.loads(result.content)

    return json_result

def get_page(token: str, json_result_items: dict, page: str) -> dict:
    if json_result_items[page] is None:
        return {"error": {
            "message": f"No {page} href"
            }
        }

    return get_json_from_href(token, json_result_items[page])