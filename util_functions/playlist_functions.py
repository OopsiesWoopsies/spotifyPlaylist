import json

from requests import get, post

from util_functions import get_token, util, searching
from random import randint


def get_playlists(token: str) -> dict:
    url = "https://api.spotify.com/v1/me/playlists"
    header = get_token.get_auth_headers(token)

    # requests to get current user's playlists
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

    # requests to create a new playlist
    data = json.dumps(data)
    result = post(url, data=data, headers=headers)
    json_result = json.loads(result.content)

    return json_result

def get_playlist_tracks(token, href: str) -> dict:
    return util.get_json_from_href(token, href)


def generate_playlist(token: str, keyword: str, song_amount: int = 30) -> None:
    if keyword == "":
        print("Nothing in keyword")
        return

    playlist_id = create_playlist(token, keyword + " playlist")["id"]
    json_result = searching.get_playlist(token, keyword)  # check keyword cases if needed
    song_id_set = set()
    # local cache of json playlist search results
    json_result_pages= {
        0: json_result["items"]
    }
    offset = 0
    addition_attempt = 0
    max_addition_attempt = 1000

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_token.get_auth_headers(token)

    # algorithm for adding songs (ensure no duplicate songs) **
    # sets offset, finds page number, and adds a randomly selected song from the randomly selected playlist
    while len(song_id_set) < song_amount and addition_attempt < max_addition_attempt:
        playlist_pick = randint(0,json_result["total"]-1)
        offset = (playlist_pick // 50) * 50
        page_index = playlist_pick // 50
        if page_index not in json_result_pages:
            json_result = searching.get_playlist(token, keyword, str(offset))
            json_result_pages[page_index] = json_result["items"]
        else:
            json_result = json_result_pages[page_index]

        playlist_pick %= 50
        playlist_tracks = json_result["items"][playlist_pick]["tracks"]
        song_pick = randint(0, playlist_tracks["total"]-1)
        href = playlist_tracks["href"]

        result = get(href, headers=headers)
        json_result = json.loads(result.content)

        # goal: create offsetting for song picking, check for song already in set (remember addition attempts), decide what to do if duplicate

    # requests to add songs on to playlist
    data = {
            "uris": list(song_id_set)
    }

    data = json.dumps(data)
    post(url, data=data, headers=headers)


def manual_add_song_to_playlist(token: str, playlist_id: str, song_id: str) -> None: # Gonna be empty for a while (not sure if feature)
    pass