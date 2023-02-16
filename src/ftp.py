from ftplib import FTP
from time import sleep
from config import get_config
from os.path import basename

def save_ftp(path):
    config = get_config()["FTP"]
    ftp = FTP()
    
    while True:
        try:
            # Connect to FTP Server and Login
            ftp.connect(config["hostname"], int(config["port"]))
            break
        except ConnectionResetError:
            sleep(500)

    # Login
    ftp.login(config["username"], config["password"])

    # Head into dir
    ftp.cwd(config["path"])

    # Get filename from path
    filename = basename(path)

    # use tmp file
    with open(path, 'rb') as file:
        # Save pdf on ftp server
        ftp.storbinary(f"STOR {filename}", file)
    
    # close connection
    ftp.close()
