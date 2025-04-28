from datetime import datetime

from dotenv import load_dotenv
import os
import base64

from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
refresh_token = os.getenv("REFRESH_TOKEN")


def encode_auth() -> str:
    auth = client_id + ":" + client_secret
    auth_bytes = auth.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    return auth_base64


def get_refresh_token() -> tuple:
    redir = "http://127.0.0.1:8888/callback"

    parameters = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redir,
        "scope": "user-read-private user-read-email user-top-read user-read-recently-played user-library-modify user-library-read playlist-modify-public playlist-modify-private playlist-read-private user-read-currently-playing playlist-read-collaborative user-modify-playback-state user-read-playback-state",
        "show_dialog": True
    }

    response = get("https://accounts.spotify.com/authorize", params = parameters)

    print(response.status_code, response.url)

    code = input("Code: ")

    auth_base64 = encode_auth()
    parameters = {
        "code": code, # USE A WEBSERVER TO TAKE CODE FROM URL
        "redirect_uri": redir,
        "grant_type": "authorization_code"
    }
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = post("https://accounts.spotify.com/api/token", params=parameters, headers=headers)
    json_result = json.loads(response.content)

    token = json_result["access_token"]
    re_token = json_result["refresh_token"]

    with open("../.env", "r") as f:
        print("enter")
        my_dict = {}
        for line in f.readlines():
            try:
                key, value = line.split('=')
                my_dict[key[:-1]] = value
            except ValueError:
                # syntax error
                print("Reading dotenv gone wrong, syntax error")
    my_dict["REFRESH_TOKEN"] = re_token
    with open("../.env", "w") as f:
        f.write("CLIENT_ID =" + my_dict["CLIENT_ID"])
        f.write("CLIENT_SECRET =" + my_dict["CLIENT_SECRET"])
        f.write("REFRESH_TOKEN = \"" + my_dict["REFRESH_TOKEN"] + "\"")

    print(json_result)
    expiry = json_result["expires_in"] + datetime.now().timestamp()
    return re_token, token, expiry


def get_token() -> tuple:
    global refresh_token
    url = "https://accounts.spotify.com/api/token"
    token = None
    expiry = None

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    headers = {
        "Authorization": "Basic " + encode_auth()
    }

    response = post(url, headers=headers, data=data)
    json_result = json.loads(response.content)

    if "error" in json_result:
        if json_result["error"] == "invalid_grant":
            print("Invalid refresh token, fetching a new one")
            refresh_token, token, expiry = get_refresh_token()
        else:
            print("ERROR: DESCRIPTION: " + json_result["error_description"])
    else:
        token = json_result["access_token"]
        expiry = json_result["expires_in"] + datetime.now().timestamp()
        print("Token fetched")

    return token, expiry


def check_expiration(token: str, expiry: float) -> tuple:
    if datetime.now().timestamp() >= expiry:
        print("Expired token, refreshing")
        token, expiry = get_token()

    return token, expiry


def get_auth_headers(token: str) -> dict:
    return {"Authorization": "Bearer " + token}