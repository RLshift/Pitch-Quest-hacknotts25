## authentication

from spotipy import Spotify 
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

import os 
import random
import time

from flask import Flask, redirect, request, session, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

client_id = '04f118aeedc64b85b6754e35aa90f0f4'
client_secret = '3467239dc34c4742bbbcc68db832e0e8'
redirect_uri = 'https://127.0.0.1:5000/callback'
scope = 'playlist-read-private, user-modify-playback-state'
tracks = []

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
    # playlists_html = '<br><br>'.join([f'{name}: {url}' for name, url in playlists_info])

    # WIP change to playlist after
    track_info = get_track_info("2UuPXwlzXhH9lUNDSeG6cq")
    return playing(track_info, 1)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# get array of track uri with playlist url
def get_track_info(playlist_uri):
    tracks = []
    # playlist_uri = playlist_url.rfind("/")
    for track in sp.playlist_tracks(playlist_uri)["items"]:
        track_uri = track["track"]["uri"]
        track_name = track["track"]["name"]
        result = track_name, track_uri
        tracks.append(result)
    return tracks

def get_track():
    print(f"\n\nPLAYING: {song_name}")
    if (song_name == 'dont_stop'):
        # Dont Stop
        sp.start_playback(uris=['spotify:track:4PCVZGch6Q57RVAcai9L8u'], position_ms=33000)
        time.sleep(11.8)
        sp.pause_playback()
        time.sleep(1)
    elif(song_name == 'nights'):
        sp.start_playback(uris=['spotify:track:0ct6r3EGTcMLPtrXHDvVjc'], position_ms=79000)
        time.sleep(6.5)
        sp.pause_playback()
        time.sleep(1)
    elif(song_name == 'kilby_girl'):
        sp.start_playback(uris=['spotify:track:1170VohRSx6GwE6QDCHPPH'], position_ms=37000)
        time.sleep(5.4)
        sp.pause_playback()
        time.sleep(1)
    elif(song_name == 'stargazing'):
        sp.start_playback(uris=['spotify:track:3Vr3zh0r7ALn8VLqCiRR10'], position_ms=39000)
        time.sleep(6.8)
        sp.pause_playback()
        time.sleep(1)
    elif(song_name == 'coulda_been_me'):
        sp.start_playback(uris=['spotify:track:3IyCL4Em1GOpNGDf451Hg1'], position_ms=39000)
        time.sleep(6.6)
        sp.pause_playback()
        time.sleep(1)

@app.route('/playing')
def playing(track_info, run_times):
    get_track()
    # sp.start_playback(uris=[ran_track[1]], position_ms=start_playing)
        # # Dont Stop
        # sp.start_playback(uris=['spotify:track:4PCVZGch6Q57RVAcai9L8u'], position_ms=33000)
        # time.sleep(11.8)
        # sp.pause_playback()
        # time.sleep(1)
    # The Nights
        # sp.start_playback(uris=['spotify:track:0ct6r3EGTcMLPtrXHDvVjc'], position_ms=79000)
        # time.sleep(6.5)
        # sp.pause_playback()
        # time.sleep(1)
    # Kilby Girl
        # sp.start_playback(uris=['spotify:track:1170VohRSx6GwE6QDCHPPH'], position_ms=37000)
        # time.sleep(5.4)
        # sp.pause_playback()
        # time.sleep(1)
    #Stargazing
        # sp.start_playback(uris=['spotify:track:3Vr3zh0r7ALn8VLqCiRR10'], position_ms=39000)
        # time.sleep(6.8)
        # sp.pause_playback()
        # time.sleep(1)
    # Coulda been me
        # sp.start_playback(uris=['spotify:track:3IyCL4Em1GOpNGDf451Hg1'], position_ms=39000)
        # time.sleep(6.6)
        # sp.pause_playback()
    ## The nights, Kilby girl, dont stop, stargazing, coulda been me 
    ##
    if (run_times-1 == 0):
        return '<br>'
    else:
        return playing(track_info, run_times-1)

def runApp(name):
    global song_name 
    song_name = name
    app.run(ssl_context=('../cert.pem', '../key.pem'))