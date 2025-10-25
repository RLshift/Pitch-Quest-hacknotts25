## Song Conversion using Spotipy Library 
### Files
[Importing Songs](/spotifyAPI.py)

## Libraries 
- Spotipy (Spotify Player's API)
- Flask

## Problems 
1. Spotify only supports https redirect URIs 
- Solution: Implement https in flask 
- Certificates: [cert.pem](cert.pem) & [key.pem](key.pem)
- [reference] (https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https)

2. User has to activate their device audio output before the program can change the song
- fixed with page authorising spotify account

3. User has to have spotify in the background for the song to change 
- magically worked during development phase
