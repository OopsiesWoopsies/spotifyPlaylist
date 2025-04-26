import json

from requests import get, post, delete, put

from util_functions import get_token, util, searching
from random import randint


def get_playlists(token: str) -> dict:
    url = util.SPOTIFY_API_URL + "/me/playlists"
    header = get_token.get_auth_headers(token)

    # requests to get current user's playlists
    result = get(url, headers=header)
    json_result = json.loads(result.content)

    return json_result


def create_playlist(token: str, playlist_name: str = "New Playlist", description: str = "", public: bool = False) -> dict:
    url = util.SPOTIFY_API_URL + "/me/playlists"
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
        print("Nothing in keyword, no playlist created")
        return


    def check_playlist_availability(pick: int) -> int:
        nonlocal json_result, addition_attempt, json_result_playlist_pages
        offset = (pick // 50) * 50
        page_index = pick // 50
        addition_attempt += 1
        pick %= 50

        if page_index not in json_result_playlist_pages:
            json_result = searching.get_playlist(token, keyword, str(offset))
            json_result_playlist_pages[page_index] = json_result

        json_result = json_result_playlist_pages[page_index]

        return pick


    def check_song_availability(pick: int) -> int:
        nonlocal json_result, local_addition_attempt, href, json_result_song_pages
        offset = (pick // 100) * 100
        page_index = pick // 100
        local_addition_attempt += 1
        pick %= 100

        if page_index not in json_result_song_pages:
            href += f"?offset={offset}"
            result = get(href, headers=headers)
            json_result = json.loads(result.content)
            json_result_song_pages[page_index] = json_result

        json_result = json_result_song_pages[page_index]

        return pick


    json_result = searching.get_playlist(token, keyword)  # check keyword cases if needed
    total_playlists = json_result["total"]
    song_id_set = set()
    # local cache of json playlist search results
    json_result_playlist_pages = {
        0: json_result
    }
    addition_attempt = 0
    MAX_ADDITION_ATTEMPT = 100
    MAX_LOCAL_ADDITION_ATTEMPT = 50
    headers = get_token.get_auth_headers(token)

    # Sets offset, finds page number, and adds a randomly selected song from the randomly selected playlist
    while len(song_id_set) < song_amount and addition_attempt < MAX_ADDITION_ATTEMPT:
        playlist_pick = randint(0,total_playlists-1)
        playlist_pick = check_playlist_availability(playlist_pick)

        # Checks if the playlist is still available
        while json_result["items"][playlist_pick] is None:
            playlist_pick = randint(0, total_playlists-1)
            playlist_pick = check_playlist_availability(playlist_pick)

        playlist_tracks = json_result["items"][playlist_pick]["tracks"]
        addition_success = 0
        local_addition_attempt = 0

        href = playlist_tracks["href"]
        result = get(href, headers=headers)
        json_result = json.loads(result.content)

        json_result_song_pages = {
            0: json_result
        }
        # Adds songs
        while addition_success < 10 and local_addition_attempt < MAX_LOCAL_ADDITION_ATTEMPT and len(song_id_set) < song_amount:
            href = playlist_tracks["href"]
            song_pick = randint(0, playlist_tracks["total"] - 1)
            song_pick = check_song_availability(song_pick)

            # Checks if the song is still available
            while json_result["items"][song_pick] is None:
                song_pick = randint(0, json_result["total"] - 1)
                song_pick = check_song_availability(song_pick)

            song = json_result["items"][song_pick]["track"]["uri"]
            if song not in song_id_set:
                song_id_set.add(song)
                addition_success += 1

    # Creates a playlist and requests to add songs on to playlist
    playlist_id = create_playlist(token, keyword + " playlist")["id"]
    url = util.SPOTIFY_API_URL + f"/playlists/{playlist_id}/tracks"
    data = {
        "uris": list(song_id_set)
    }

    data = json.dumps(data)
    post(url, data=data, headers=headers)


def remove_playlist_from_library(token: str, playlist_id: str) -> None:
    url = util.SPOTIFY_API_URL + f"/playlists/{playlist_id}/followers"
    headers = get_token.get_auth_headers(token)

    delete(url, headers=headers)


def edit_playlist(token: str, playlist_id: str, field_change: str, new_field: str) -> None:
    url = util.SPOTIFY_API_URL + f"/playlists/{playlist_id}"
    headers = get_token.get_auth_headers(token)
    data = {
        field_change: new_field
    }

    data = json.dumps(data)
    put(url, headers=headers, data=data)