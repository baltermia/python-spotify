from configparser import ConfigParser

__configPath = "config.ini"

def get_config(path = __configPath):
    config = ConfigParser()
    config.read(path)
    
    return config

def save_config(config, path = __configPath):
    with open(path, "w") as conf:
        config.write(conf)
    return