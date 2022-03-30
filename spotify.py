import enum
from sys import float_repr_style
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util


cid = '5ea48a8853c5458b8a8750ab7acf3b63'
secret = '0469eddbfe5e4543a2b4915f6b3e65c9'
username = 'najtechnologies'
redirect_uri = 'http://localhost:8080'

scope = 'user-top-read'

token = util.prompt_for_user_token(username,scope,cid,secret,redirect_uri)

sp = spotipy.Spotify(auth=token)
playlists=sp.current_user_playlists()

user_id = sp.me()['id']
top='37i9dQZEVXbMDoHDwVN2tF'

cont =0
while playlists:
    for i, playlist in enumerate(playlists['items']):
       
        tracks=[]
        result = sp.playlist_tracks(top, additional_types=['track'])
        
        tracks  =  result['items']
      
        while result['next']:
            result = sp.next(result)
            tracks.extend(result['items'])

        for j in tracks:
            cont +=1;
            print(cont, j['track']['name'],'//', j['track']['artists'][0]['name'])       
        
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
data = {}

data = tracks







