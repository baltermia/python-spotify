
from configparser import ConfigParser

__configPath = "config.ini"

__config = None

def get_config(path = __configPath):
    __configPath = path

    if __config is None:
        __config = ConfigParser()
        __config.read(path)
    
    return __config

def save_config(config, path = __configPath):
    if config is not ConfigParser:
        return

    __config = config
    return