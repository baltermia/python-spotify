<h1 align=center>Main Documentation</h1>

Spotify to PDF converts a Spotify playlist into a PDF file. After starting the Python script the user will be prompted and asked for information to find the playlist he wants to be converted. He can either enter a link directly, a playlist name with the creator or just a keyword which the script will use to determine a playlist. Using the [Spotify API](https://developer.spotify.com/documentation/web-api/) all playlist data (playlist name, songs etc.) which is then written into a PDF file.

## Requirements
- Use a public API
- Create PDF files from the response data
- Upload the PDf on a FTP server
- Send the PDF per email

## Steps
<img src=https://github.com/baltermia/spotify-to-pdf/blob/main/docs/steps.drawio.png />

## Template
View the PDF template [here](https://github.com/baltermia/spotify-to-pdf/blob/main/docs/template.pdf).

## Calling script
Using all parameters:
```
spotify-to-pdf.py <playlist_id> <email> <username> <password>
```

Using default email:
```
spotify-to-pdf.py <playlist_id> <username> <password>
```

Using default credentials:
```
spotify-to-pdf.py <playlist-id> <email>
```

Using default credentials and default email:
```
spotify-to-pdf.py <playlist-id>
```

Default credentials are set in a seperate config file (json).
