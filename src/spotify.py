from config import get_config, save_config

__config = None

__token = None

def __manage_access():
    client_id = __config["SPOTIFY"]["cid"]
    client_secret = __config["SPOTIFY"]["secret"]
    return

def get_playlist(id):
    __config = get_config()

    __manage_access()

    return
