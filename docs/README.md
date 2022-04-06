<h1>Documentation</h1> <!-- using html instead of # prevents table of contents to include first header -->

> This documentation is and should be written before any development starts

Spotify to PDF converts a Spotify playlist into a PDF file. After starting the Python script the user will be prompted and asked for information to find the playlist he wants to be converted. He can either enter a link directly, a playlist name with the creator or just a keyword which the script will use to determine a playlist. Using the [Spotify API](https://developer.spotify.com/documentation/web-api/) all playlist data (playlist name, songs etc.) which is then written into a PDF file.

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Requirements](#requirements)
- [Steps](#steps)
- [Template](#template)
- [API](#api)
- [Config](#config)
  - [Config file](#config-file)
    - [Using `ConfigParser`](#using-configparser)
      - [Read](#read)
      - [Write / Update](#write--update)
    - [File structure](#file-structure)
  - [Config Credentials](#config-credentials)
    - [Spotify Credentials](#spotify-credentials)
    - [SendGrid API Key](#sendgrid-api-key)
    - [FTP Credentials](#ftp-credentials)
- [Python Modules](#python-modules)
  - [Spotify API](#spotify-api)
    - [Authorization](#authorization)
      - [Token Expiration](#token-expiration)
    - [Get Playlist](#get-playlist)
    - [Get songs](#get-songs)
  - [SendGrid API](#sendgrid-api)
    - [PDF to Base64](#pdf-to-base64)
  - [Save File on FTP](#save-file-on-ftp)
  - [Create PDF File](#create-pdf-file)
  - [File Parameters](#file-parameters)

## Requirements
- Use a public API
- Create PDF files from the response data
- Upload the PDF on a FTP server
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

No credentials should be provided. All configuration data should be set in [config.ini](https://github.com/baltermia/spotify-to-pdf/tree/main/src/config_template.ini) config file.

## Config

### Config file

Configuration files are being managed with the `ConfigParser` python library.

#### Using `ConfigParser`

First import library and create object
```python
from configparser import ConfigParser

# Create new object
config = ConfigParser()
```

##### Read

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

##### Write / Update

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

#### File structure

The config file should be saved under [src](https://github.com/baltermia/spotify-to-pdf/tree/main/src) as `config.ini`.

```python
# Crendentials for the default spotify account with which the api is accesed
[SPOTIFY]
cid = 
secret =
token =
token_expiration =

# API key for SendGrid API
[SENDGRID]
api_key =

# Credentials to connect to FTP server
[FTP]
hostname = 
port = 
username = 
password =
path =
```

### Config Credentials

Following credentials are neccessary for the script:
- Spotify App credentials (not login)
- Mail Accout with SMTP
- FTP Server login

#### Spotify Credentials

Sending requests to the spotify api requires a access token. The spotify access token expires after 1 hour, therefore a new token needs to be requested again after some time. 

The spotify acces_token can be requested using a spotify app login. This login is different from a regular spotify login. A app needs to be created under the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).

<img src=https://github.com/baltermia/spotify-to-pdf/blob/main/docs/resources/spotify-credentials-flow.png width=500 />

The `token_expiration` property holds the datetime value when the `token` expires.

#### SendGrid API Key

To use the SendGrid API all we need is an api_key. We can get this when we create a 'Single Sender' and then generate a API key for that.

#### FTP Credentials

The FTP Server credentials are simple. Get the login details and the server address and port.
Any FTP Server can be used, for this project https://bplaced.net is being used.

We also set a `path` in the config. This leads to the directory on the FTP server where the files should be stored in.

## Python Modules

### Spotify API

First, to do any web requests we need to import the `requests` module
```python
import requests
```

#### Authorization

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

The response also includes a `expires_in` value. After the token expires, a new one needs to be requested (see more under [Token Expiration](#token-expiration)). In the meantime, the token can be [stored in the config file](#write--update).

In the end, a global `headers` dictionary should be created that contains the bearer token as authorization value
```python
headers = {
    'Authorization': 'Bearer {}'.format(token)
}
```
These headers are sent with every request to authorize the requests.

##### Token Expiration

The access token we recieve from the spotify accounts api expires after 1 hour. When we get a new token, we recieve a `expires_in` value. This holds the amount of seconds from now when the token will expire.

We will convert this this to a datetime value that we willstore in the config file using [Config-Write/Update](#write--update). The script checks this date before any request, to make sure that the token is still valid.

The following code will create us the datetime and parse it:

First import the required modules
```python
from datetime import datetime, timedelta
```

Get the datetime object
```python
expiration = reponse.json().get("expires_in")

date = datetime.now() + timedelta(seconds = expiration)

# Here we would write the date into the config file
```

When reading the date from the config, we want to check if it is already past the curent time
```python
date_str = # get date from config

exp_date = datetime.strptime(date_str)

if datetime.now() >= exp_date:
    # token expired. request a new one
```

#### Get Playlist

The only request besides authorization is getting the playlists. The request for this is quite easy, given that we have the playlist ID.

First though, we set a base url that is used for every request
```python
base_url = "https://api.spotify.com/v1/"
```

Then we get the playlist
```python
playlist_id = "<some_id>"

response = requests.get(base_url + "playlists/" + playlist_id, headers = headers)

# Whole response json
playlist = response.json()

# Get playlist name
name = playlist.get("name")
```

The rest of the playlist api endpoint (e.g. whole response body) can be found [here](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-playlist)

#### Get songs

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

### SendGrid API

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

Head to [PDF to Base64](#pdf-to-base64) below to see how to convert a PDF file to a Base64 string.

And finally we make the request
```python
api_key = "<api-key>"

client = SendGridAPIClient(api_key)

response = sg.send(mail)
```

#### PDF to Base64

First we need the following import
```python
from base64 import b64encode
```

Then, we can easily convert the pdf to base64
```python
path = "<pdf-location>"

with open(path, "rb") as pdf_file:
    encoded = b64encode(pdf_file.read())
```
The pdf is now encoded as base64 string in the `encoded` object.

### Save File on FTP

We don't use a API to save files on a FTP Server. (That would take the point of FTP)

First we import the library
```python
from ftplib import FTP_TLS
```

Then we can create a new ftp object
```python
ftp = FTP_TLS()
```

We can then conntect and login to that server
```python
ftp.connect("<hostname>", "<port>")

ftp.login("<username>", "<password>")
```

And head into a directory
```python
ftp.cwd("<path>")
```

And finally save the pdf file
```python
path = "<pdf-location>"

with open(path, "rb") as pdf_file:
    ftp.storbinary("STOR <filename>", pdf_file)
```

If we don't need the `ftp` object anymore, we can close it
```python
ftp.close()
```

### Create PDF File

For creating the PDF exports we use the library [FPDF](https://pyfpdf.readthedocs.io/). It adds a very simple API to python for creating pdf files.

First we need to import the library
```python
from fpdf import FPDF
```

Then we create a new pdf object and add some properties to it
```python
pdf = FPDF() # Default is Portrait, A4

pdf.set_font("<your-font>", "<weight>", "<size>")
```

Before we start adding things to the pdf, we have to add a page
```python
pdf.add_page()
```

Then we can easily add some text with margin to the topleft corner
```python
pdf.cell(40, 10, "<your-text>")
``` 

We can also add iamges
```python
pdf.image(name = "<img_url>", x = "<topleft-margin>", y = "<topleft-margin>", h = "<height>", width = "width")
```

Finally, we can save the pdf
```python
pdf.output("<path>")
```

Or you can get the bytestring
```python
pdf_bytes = pdf.output(dest="S")
```

### File Parameters
You can access parameters that are given when calling the file like this:

```python
first = sys.argv[0]
second = sys.argv[1]
```

There's a better way to handle arguments though
```python
def test(first, second):
    # Your code here    
    
if __name__ == '__main__':   # will only run when the script is run directly (good practice)
    test(sys.argv[0], sys.argv[1])
```

Remember to import the library
```python
import sys
```
