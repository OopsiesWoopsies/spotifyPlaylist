from datetime import datetime

from dotenv import load_dotenv
import os
import base64

from flask import Flask, request
import webbrowser
import multiprocessing
import asyncio

from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
test_refresh_token = os.getenv("TEST_REFRESH_TOKEN")


def run_flask(shared_auth_code) -> None:
    """
    Creates and runs a flask server.
    :param shared_auth_code: Variable for authorization code for future use.
    :return: None
    """

    app = Flask(__name__)

    @app.route("/callback")
    def callback() -> str:
        """
        Handles OAuth 2.0 callback.
        :return: A message to appear on the web page.
        """

        code = request.args.get("code")
        shared_auth_code.value = code or ""
        return "Authorization complete"

    app.run(host="0.0.0.0",port=5000, use_reloader=False)


async def login(url: str) -> str:
    """
    Runs a flask server to get user's permission to use their spotify data.
    :param url: The url that allows user to authenticate their Spotify account.
    :return: The authorization code.
    """

    # Creates a shared variable so the flask process can pass it back to the main process
    manager = multiprocessing.Manager()
    auth_code = manager.Value(str, "")
    flask_process = multiprocessing.Process(target=run_flask, args=(auth_code,), daemon=True)
    flask_process.start()

    webbrowser.open_new(url)

    while auth_code.value == "":
        await asyncio.sleep(1)

    flask_process.terminate()
    return auth_code.value


def get_auth_headers(token: str) -> dict:
    """
    Authorization header necessary for a Spotify api request.
    :param token: A Spotify access token.
    :return: Authorization header for Spotify api requests.
    """

    return {"Authorization": "Bearer " + token}


def encode_auth() -> str:
    """
    Encodes client id and client secret into a base 64 string for Spotify authorization.
    :return: Base 64 encoded string.
    """

    auth = client_id + ":" + client_secret
    auth_bytes = auth.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    return auth_base64


async def get_refresh_token() -> tuple:
    """
    Sends a request to Spotify api for a refresh token, access token, and expiry for the token.
    :return: A refresh token, Spotify access token, and expiry time for the said token.
    """

    redir = "http://localhost:5000/callback"

    parameters = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redir,
        "scope": ("user-read-private user-read-email user-top-read "
                  "user-read-recently-played user-library-modify "
                  "user-library-read playlist-modify-public "
                  "playlist-modify-private playlist-read-private "
                  "user-read-currently-playing playlist-read-collaborative "
                  "user-modify-playback-state user-read-playback-state"),
        "show_dialog": True
    }

    # Sends an authorization request to Spotify api
    response = get("https://accounts.spotify.com/authorize", params = parameters)
    auth_code = await login(response.url)

    auth_base64 = encode_auth()
    parameters = {
        "code": auth_code,
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
    expiry = json_result["expires_in"] + datetime.now().timestamp()

    return re_token, token, expiry


def get_token(refresh_token: str, test: bool = False) -> tuple:
    """
    Sends a request to the Spotify api for a Spotify token using the Spotify refresh token.
    :param refresh_token: Spotify refresh token.
    :param test: Indicates testing. Default: False.
    :return: A Spotify access token and the expiry time for said token.
    """

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

    # Sends a request to Spotify api for a user token
    response = post(url, headers=headers, data=data)
    json_result = json.loads(response.content)

    # Checks for error when using refresh token
    if "error" in json_result:
        if json_result["error"] == "invalid_grant":
            refresh_token, token, expiry = asyncio.run(get_refresh_token())
            if test:
                write_to_env(refresh_token)
        else:
            print("ERROR: DESCRIPTION: " + json_result["error_description"])
    else:
        token = json_result["access_token"]
        expiry = json_result["expires_in"] + datetime.now().timestamp()

    return token, expiry


def check_expiration(token: str, refresh_token: str, expiry: float) -> tuple:
    """
    Checks if the Spotify token needs to be renewed.
    :param token: Spotify access token.
    :param refresh_token: Spotify refresh token.
    :param expiry: Expiry time for the Spotify token.
    :return: A valid Spotify access token and the expiry time for said token.
    """

    if datetime.now().timestamp() >= expiry:
        token, expiry = get_token(refresh_token)

    return token, expiry


def write_to_env(refresh_token: str) -> None:
    """
    Writes key information to the .env file.
    :param refresh_token: Spotify refresh token.
    :return: None.
    """

    # Replaces the old refresh token with the newly retrieved one
    with open("../.env", "r") as f:
        my_dict = {}
        for line in f.readlines():
            try:
                key, value = line.split('=')
                my_dict[key[:-1]] = value
            except ValueError:
                # syntax error
                print("Reading dotenv gone wrong")
    with open("../.env", "w") as f:
        f.write("CLIENT_ID =" + my_dict["CLIENT_ID"])
        f.write("CLIENT_SECRET =" + my_dict["CLIENT_SECRET"])
        f.write("DISCORD_BOT_TOKEN =" + my_dict["DISCORD_BOT_TOKEN"])
        f.write("DISCORD_SERVER_ID =" + my_dict["DISCORD_SERVER_ID"])
        f.write("TEST_REFRESH_TOKEN = \"" + refresh_token + "\"")