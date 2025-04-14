from util_functions import get_token

from requests import get
import json


def search_for_artist(token: str, artist_name: str):
    limit = 5
    url = "https://api.spotify.com/v1/search"
    headers = get_token.get_auth_headers(token)
    query = f"?q={artist_name}&type=artist&limit={limit}" #artist,track (if looking for track as well)

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    return json_result

def get_songs(token: str, artist_id: str):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=CA"
    headers = get_token.get_auth_headers(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result