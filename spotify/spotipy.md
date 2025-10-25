## Song Conversion using Spotipy Library 
### Files
[Importing Songs](/spotifyAPI.py)
[Testing API](/index.html)

## Before running program 
- pip install spotipy library

## Problems 
1. Spotify only supports https redirect URIs 
- Solution: Implement https in flask 
- Certificates: [cert.pem](cert.pem) & [key.pem](key.pem)
- [reference] (https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https)

2. User has to activate their device audio output before the program can change the song

3. User has to have spotify in the background for the song to change 
NOTE -- Music can be changed but not implemented (currently only playing "NF - Let you down" once "/get_playlists" page is loaded)