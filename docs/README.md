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

## Using Spotify API
The request are being made with the opensource python library [spotipy](https://github.com/plamere/spotipy)

### Spotipy
Importing:
```python
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
```

Get spotify object with authentication
```python
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="<username>", client_secret="<password>"))
```

Get playlist
```python
pl = sp.playlist("<playlist_id>")

name = pl["name"]
uri = pl["uri"]
# etc..
```

## Config file

Configuration files are being managed with the `ConfigParser` python library. There's no need for writing configurations, the parser only reads it.

### Using `ConfigParser`

First import library and create object
```python
from configparser import configParser

config = ConfigParser();
```

Then we read the file using a static path
```python
config.read("config.ini")
```

The config file has multiple sections. (See [File structure](#file-structure) below)
Get a section and value
```python
fdp = config["FDP"] # get section
ip = fdp["ip"]      # get value
```

### File structure

The config file should be saved under [src](https://github.com/baltermia/spotify-to-pdf/tree/main/src) as `config.ini`.

```python
# Crendentials for the default spotify account with which the api is accesed
[SPOTIFY]
cid = 
secret =

# Credentials for email-account to send mails
[EMAIL]
mail = 
password =
smtp =
port =

# Credentials to connect to FDP server
[FDP]
hostname = 
port = 
username = 
password =
```