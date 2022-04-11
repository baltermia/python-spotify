from config import get_config, save_config
import requests
from datetime import datetime, timedelta

def get_headers():
    config = get_config()
    c_spotify = config["SPOTIFY"]

    if datetime.now() < datetime.strptime(c_spotify["token_expiration"]):
        return {
            'Authorization': 'Bearer {}'.format(c_spotify["token"])
        } 

    client_id = c_spotify["cid"]
    client_secret = c_spotify["secret"]

    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }

    response = requests.post("https://accounts.spotify.com/api/token", data)

    token = response.json().get("access_token")
    expiration = response.json().get("expires_in")

    c_spotify["token"] = token
    c_spotify["expiration"] = datetime.now() + timedelta(seconds = expiration)

    save_config()

    return {
        'Authorization': 'Bearer {}'.format(token)
    }

def get_playlist(id):
    headers = get_headers()

    response = requests.get("https://api.spotify.com/v1/playlists/" + id, headers = headers)

    return response.json()
