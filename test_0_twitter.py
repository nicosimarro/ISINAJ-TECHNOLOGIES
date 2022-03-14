#!/usr/bin/env python3

import requests

URI_API = 'https://api.twitter.com'

#ultimos tweets de un usuario
user_uri = '/2/tweets/search/recent?query=from:IbaiLlanos'

#ultimos tweets de una busqueda
tweets_uri = '/2/tweets/search/recent'


'''Buscar un tweets recientes'''
try:
    parametros = {
        'query' : 'Dakiti'
    }
    header = {
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAC7qaAEAAAAACqCHqNLHGRybM6LTsp252Lo6rjQ%3DzXNnncdySA8L6wsZGu7e6fBfetpFVlwlIzpLAkhUr6upi9DP9S'
    } 
    response = requests.get(URI_API+tweets_uri, headers=header, params=parametros)
    if response.status_code == 200:
        print(response.content.decode())
    else:
        print(response.content.decode())
except requests.models.MissingSchema: #pragma: no cover
    raise ServerError('Wrong URL format') from requests.models.MissingSchema
