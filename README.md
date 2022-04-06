<div align=center>
  <h1>🎉Spotify to PDF</h1>
  A python script that creates PDF Files from Spotify playlists.
</div>

### [Documentation](https://github.com/baltermia/spotify-to-pdf/tree/main/docs#documentation)

## Imports
```
pip install configparser
pip install sendgrid
```

## Setup

This program won't work on its own. Follow the steps below.

### Create `Config.ini`

First we need to create the `config.ini` file. There's a template of the file under [/src/config_template.ini](https://github.com/baltermia/spotify-to-pdf/blob/main/src/config_template.ini). Copy this file under the filename `config.ini` and populate it with the crendentials listed below.

### Spotify Credentials

1. Head to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard/) and login
2. Accept the Developer Terms of Service
3. In the Dashboard click the `Create an APP` button on the top right
4. Call it Spotify-to-PDF (or whatever you like)
5. Click create
6. Copy and paste the `Client ID` and `Client ecret` into the config file

Spotify is now setup!


### SendGrid API Key

1. Create an account or login at [sendgrid.com](https://sendgrid.com())
2. Create a new API Key on the [API Dashboard](https://app.sendgrid.com/settings/api_keys)
3. Make sure you have a Single Sender address verificated (under Settings/Sender Authentication)

If you're unsure on what to do, head to the [general](https://app.sendgrid.com/guide) or [python](https://app.sendgrid.com/guide/integrate/langs/python) guide.

### FTP Server

You can use any FTP Server you would like. There are a lot of free services, one of them is [bplaced.net](https://www.bplaced.net/). 

Go on the dashboard of your hosting service and get your hostname, port, username and password and paste them into the config file.
