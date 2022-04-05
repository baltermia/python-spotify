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
from configparser import ConfigParser

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

## Spotify API

First, to do any web requests we need to import the `requests` module
```python
import requests
```

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

Then make a post request with the data
```python
reponse = requests.post("<auth_url>", data)
```

And after that, we can get the access token from the json
```python
token = reponse.json().get("access_token")
```

The response also includes a `expires_in` value. After the token expires, a new one needs to be requested. In the meantime, the token can be [stored in the config file](#write--update).

In the end, a global `headers` dictionary should be created that contains the bearer token as authorization value
```python
headers = {
    'Authorization': 'Bearer {}'.format(token)
}
```
These headers are sent with every request to authorize the requests.

### Get Playlist

The only request besides authorization is getting the playlists. The request for this is quite easy, given that we have the playlist ID.

First though, we set a base url that is used for every request
```python
base_url = "https://api.spotify.com/v1/"
```

Then we get the playlist
```python
playlist_id = "<some_id>"

response = requests.get(base_url + "playlists/" + playlist_id, header = headers)

# Whole response json
playlist = response.json()

# Get playlist name
name = playlist.get("name")
```

The rest of the playlist api endpoint (e.g. whole response body) can be found [here](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-playlist)

### Get songs

The `playlist` json we got in the request [above](#get-playlist) does not include tracks. What it includes though is a url we can make another request to that returns all tracks.
```python
tracks_url = playlist.get("tracks").get("href")
```

With this url we can make another request, that returns all the tracks of the playlist
```python
response = requests.get(track_url, headers = headers)

tracks = response.json().get("items")

# Get first track
first = tracks[0].get("track")
name = first.get("name")
```

## SendGrid API

To send emails we use a tool named [SendGrid](https://sendgrid.com/). We can send emails using their API. The account creation process is very straightforward and well-documented on the site. We get the api-key from there.

To use the api, we first import the required modules
```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
```

Then we can easily create a new mail
```python
mail = Mail(
    from_email='sender@main',
    to_emails='reciever@other',
    subject='SendGrid Email. Yay',
    html_content='<strong>This is your HTML content</strong>')
)
```

You can also add a attachment
```python
message.attachment = Attachment(FileContent('<base64 encoded pdf>'),
    FileName('<filename>.pdf'),
    FileType('application/pdf'),
    Disposition('attachment')
```

And finally we make the request
```python
api_key = "<api-key>"

client = SendGridAPIClient(api_key)

response = sg.send(mail)
```
