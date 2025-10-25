## authentication

from spotipy import Spotify 
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

import os 

from flask import Flask, redirect, request, session, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

client_id = '06d3f79e124a42bea66225da339d210f'
client_secret = 'ba00699a77aa43238fa6b022ff19ca71'
redirect_uri = 'https://127.0.0.1:5000/callback'
scope = 'playlist-read-private, user-modify-playback-state'

cache_handler = FlaskSessionCacheHandler(session)

sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri, 
    scope=scope, 
    cache_handler=cache_handler, 
    show_dialog=True 
)

sp = Spotify(auth_manager=sp_oauth)

@app.route('/')
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_playlists'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_playlists'))

@app.route('/get_playlists')
def get_playlists():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    playlists = sp.current_user_playlists()
    playlists_info = [(pl['name'], pl['external_urls']['spotify']) for pl in playlists['items']]
    print("#######################################")
    print(playlists_info)
    print("#######################################")
    playlists_html = '<br><br>'.join([f'{name}: {url}' for name, url in playlists_info])

    sp.start_playback(uris=['spotify:track:52okn5MNA47tk87PeZJLEL'])


    return playlists_html

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))