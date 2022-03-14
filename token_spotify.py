#!/usr/bin/env python3

import requests
import sys

#https://accounts.spotify.com/es-ES/authorize?client_id=60d57f2c190f4b76afe1baf753aa26a8&redirect_uri=http://localhost:8888/&response_type=code
#try:
#    datos = {
#        "response_type": 'code',
#        "client_id": "60d57f2c190f4b76afe1baf753aa26a8",
#        "redirect_uri": "http://localhost:8888/",
#    }
#    response = requests.get('https://accounts.spotify.com/es-ES/authorize?client_id=60d57f2c190f4b76afe1baf753aa26a8&redirect_uri=http://localhost:8888/&response_type=code')
#    if response.status_code == 200:
        #print(response.content.decode())
#        print(response.headers)
#    else: #pragma: no cover
        #raise ServerError('Non-200 response from server, aborting...')
#        print(response.content.decode())
#except requests.models.MissingSchema: #pragma: no cover
#    raise ServerError('Wrong URL format') from requests.models.MissingSchema
def get_token(code):
    '''Pedir access token'''
    try:
        token_data = {
            "grant_type":    "authorization_code",
            "code":          code,
            "redirect_uri":  "http://localhost:8888/",
            "client_secret": "6b9bc9560fd54e169005959672437567",
            "client_id":     "60d57f2c190f4b76afe1baf753aa26a8",
        }
        response = requests.post('https://accounts.spotify.com/api/token', data=token_data)
        if response.status_code == 200:
            dictionary = response.content
            print(dictionary)

            #print(str(dictionary["access_token"]))
            #token = dictionary["access_token"]
            #print(token)
        else: #pragma: no cover
            print(response.content.decode())
    except requests.models.MissingSchema: #pragma: no cover
        raise ServerError('Wrong URL format') from requests.models.MissingSchema

if __name__ == "__main__":
   get_token(sys.argv[1])