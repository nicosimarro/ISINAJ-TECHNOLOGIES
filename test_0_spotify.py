#!/usr/bin/env python3

import requests

playlist_uri = '/v1/playlists/37i9dQZF1DXaxEKcoCdWHD/tracks'
URI_API = 'https://api.spotify.com'

'''Conseguir la playlist exitos españa'''
try:
    header = {
        'Authorization': 'Bearer BQAzYbnoUdarynVaw8VOBTUuufv-tsXm4aQYTVOdmQow_CqdKU7nvl8QE9B9SseMSSSiWSxbBXNLMdcHv-6CiY-HMb8n5PQ_x94_cgJ42WUiUsehYZbMwjlkBAl3YhyL-zK246Znbum8SGY'
    } 
    response = requests.get(URI_API+playlist_uri, headers=header)
    if response.status_code == 200:
        print(response.content.decode())
    else:
        print(response.content.decode())
except requests.models.MissingSchema: #pragma: no cover
    raise ServerError('Wrong URL format') from requests.models.MissingSchema