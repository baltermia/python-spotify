from ftplib import FTP
from config import get_config
from datetime import datetime

def save_pdf(pdf, name):
    # Filename template: '<playlist-name>_<current_datetime>.pdf'
    filename = "{}_{}.pdf".format(name, datetime.now().isoformat())

    config = get_config()["FTP"]
    ftp = FTP()
    
    # Connect to FTP Server and Login
    ftp.connect(config["hostname"], int(config["port"]))
    ftp.login(config["username"], config["password"])

    # Head into dir
    ftp.pwd(config["path"])

    # Save pdf on ftp server
    ftp.storbinary(f"STOR {filename}", pdf)

    # close connection
    ftp.close()
