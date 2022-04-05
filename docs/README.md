<h1 align=center>Main Documentation</h1>

Spotify to PDF converts a Spotify playlist into a PDF file. After starting the Python script the user will be prompted and asked for information to find the playlist he wants to be converted. He can either enter a link directly, a playlist name with the creator or just a keyword which the script will use to determine a playlist. Using the [Spotify API](https://developer.spotify.com/documentation/web-api/) all playlist data (playlist name, songs etc.) which is then written into a PDF file.

> This documentation is and should be written before any development starts

## Requirements
- Use a public API
- Create PDF files from the response data
- Upload the PDf on a FTP server
- Send the PDF per email

## Steps
<details>
    <summary>Click to show diagram</summary>
    <img src=https://github.com/baltermia/spotify-to-pdf/blob/main/docs/steps.drawio.png />
</details>

## Template
View the PDF template [here](https://github.com/baltermia/spotify-to-pdf/blob/main/docs/template.pdf).

## API

```python
python spotify-to-pdf.py "<playlist-id>" "<email>"
```

- **playlist-id**: ID of the playlist (found in url as _open.spotify.com/playlist/**playlist-id**_)
- **email**: Where a mail should be sent to inculding the created PDF

No credentials should be provided. All configuration data should be set in [config.ini](https://github.com/baltermia/spotify-to-pdf/tree/main/src/config.ini) config file.

## Config file

Configuration files are being managed with the `ConfigParser` python library.

### Using `ConfigParser`

First import library and create object
```python
from configparser import configParser

# Create new object
config = ConfigParser()
```

#### Read

Then we read the file using a static path
```python
# Read file into object
config.read("config.ini")
```

The config file has multiple sections. (See [File structure](#file-structure) below)
Get a section and value
```python
ftp = config["FTP"] # get section
ip = ftp["ip"]      # get value
```

#### Write / Update

Create a new section
```python
# Set new key with dictionary
config["NEW"] = {
    "field": "value"
}

# Write the changes to the file
with open('config.ini', 'w') as conf:
    config.write(conf)
```

Update value of existing key
```python
# Read file into object
config.read("config.ini")

# Assign new value to existing key
config["NEW"]["field"] = "new value"

# Write the changes to the file
with open('config.ini', 'w') as conf:
    config.write(conf)
```

### File structure

The config file should be saved under [src](https://github.com/baltermia/spotify-to-pdf/tree/main/src) as `config.ini`.

```python
# Crendentials for the default spotify account with which the api is accesed
[SPOTIFY]
cid = 
secret =
token =

# Credentials for email-account to send mails
[EMAIL]
mail = 
password =
smtp =
port =

# Credentials to connect to FTP server
[FTP]
hostname = 
port = 
username = 
password =
```

## Config Credentials

Following credentials are neccessary for the script:
- Spotify App credentials (not login)
- Mail Accout with SMTP
- FTP Server login

### Spotify Credentials

Sending requests to the spotify api requires a access token. The spotify access token expires after some time, therefore a new token needs to be requested again after some time. 

The spotify acces_token can be requested using a spotify app login. This login is different from a regular spotify login. A app needs to be created under the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).

<img src=https://github.com/baltermia/spotify-to-pdf/blob/main/docs/resources/spotify-credentials-flow.png width=500 />

### Mail Account with SMTP

Mails can be sent using a gmail account and the gmail smpt server & port.

**Gmail SMPT Server:** `smtp.gmail.com`
**Gmail SMPT Port:** `465` (port 465 when using ssl)

The username and password are simply the email and account password. No app credentials are needed.

### FTP Credentials

The FTP Server credentials are simple. Get the login details and the server address and port.
Any FTP Server can be used, for this project https://bplaced.net is being used.

## Using Spotify API

### Authorization

After getting the spotify app credentials you can request a access token from the api. 

**URL:** https://accounts.spotify.com/api/token

The credentials can be put in a dictionary:
```python
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
}
```

`grant_type` is always 'client_credentials' when using a app login.
