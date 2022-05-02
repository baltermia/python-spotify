from ftplib import FTP
from config import get_config
from datetime import datetime

def save_pdf(pdf, name):
    # Filename template: '<playlist-name>_<current_datetime>.pdf'
    filename = "{}_{}.pdf".format(name.replace(' ', '_'), datetime.now().isoformat().replace(':', '.'))
    tmp_path = "__tmp__/{}".format(filename)

    config = get_config()["FTP"]
    ftp = FTP()
    
    # Connect to FTP Server and Login
    ftp.connect(config["hostname"], int(config["port"]))
    ftp.login(config["username"], config["password"])

    # Head into dir
    ftp.cwd(config["path"])

    # write tmp file
    with open(tmp_path, 'xb') as file:
        file.write(pdf)

    # use tmp file
    with open(tmp_path, 'rb') as file:
        # Save pdf on ftp server
        ftp.storbinary(f"STOR {filename}", file)
    
    # close connection
    ftp.close()
