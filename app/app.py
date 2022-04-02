# -*- encoding: utf-8 -*-
"""
NAJ-Technologies
"""


# import Flask 
# Flask modules
import requests
import json
from flask   import render_template, request
from jinja2  import TemplateNotFound
import enum
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

import pandas as pd
from pydataset import data
import re

import seaborn as sns
import matplotlib.pyplot as plt
from bokeh.io import output_notebook, show
from bokeh.charts import Histogram, Scatter
import folium

from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sys
from string import Template
import jwt
from datetime import datetime, timedelta

# Inject Flask magic

app = Flask(__name__)

# App Config - the minimal footprint
app.config['TESTING'   ] = True 
app.config['SECRET_KEY'] = 'S#perS3crEt_JamesBond'
file_path = os.path.abspath(os.getcwd())+ "/usuarios.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + file_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db = SQLAlchemy(app)

TOKEN_USER = None


class User(db.Model):
    db.create_all()
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(80))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    try:

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( path, segment=segment )
    
    except TemplateNotFound:
        return render_template('page-404.html'), 404

 
@app.route("/register", methods=['POST'])
def register():
    # Detect the current page
    segment = get_segment( request )
    
    #coge los valores de register.html
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    
    
    user = User(
        username = username,
        email = email,
        password = generate_password_hash(password),
        fs_uniquifier = str(uuid.uuid4())
    )
    
    db.session.add(user)
    db.session.commit()
    print(username)
    print(email)
    print(password)

    return render_template( '/login.html', segment=segment )

@app.route("/login", methods=['POST'])
def login():
    # Detect the current page
    segment = get_segment( request )
    
    # Coger usuarios de la base de datos
    users = User.query.all()
    
    username = request.form.get("username")
    password = request.form.get("password")
    
    for user in users:
        if(user.username==username and check_password_hash(user.password, password)):
            token = jwt.encode({
                'user_id': user.fs_uniquifier,
                'exp': datetime.utcnow() + timedelta(minutes = 60)
            }, app.config['SECRET_KEY'])
            # Devuelve el token para las funciones que necesiten autenticar el usuario
            # con la cabecera 'x-access-token' al hacer la peticion
            #return make_response(jsonify({'token': token.decode('UTF-8')}), 201)
            TOKEN_USER = token.decode('UTF-8')
            return render_template( '/index.html', segment=segment )

    return make_response(jsonify({"result":"User not found or password incorrect"}), 400)

    #return render_template( '/index.html', segment=segment )


# PARA DEVOLVER EL TOKEN
@app.route("/getsecrets", methods=['GET'])
def getsecrets():
    token = None
    if 'x-access-token' in request.headers:
        token = request.headers['x-access-token']
    else:
        return make_response(jsonify({"result":"Something was wrong!"}), 400)
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'])
        current_user = User.query.filter_by(fs_uniquifier = data['user_id']).first()
    except:
        return make_response(jsonify({"result":"Something was wrong with the token!"}), 400)

    return make_response(jsonify({"result":"carpe diem"}), 201)

@app.route("/spotify", methods=['POST'])
def spotify():
    cid = '5ea48a8853c5458b8a8750ab7acf3b63'
    secret = '0469eddbfe5e4543a2b4915f6b3e65c9'
    username = 'najtechnologies'
    redirect_uri = 'http://localhost:8080'
    scope = 'user-top-read'
    token = util.prompt_for_user_token(username,scope,cid,secret,redirect_uri)
    sp = spotipy.Spotify(auth=token)
    playlists=sp.current_user_playlists()
    top='37i9dQZEVXbMDoHDwVN2tF'
    
    
    data = ''
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
                cont +=1
                #print(cont, j['track']['name'],'//', j['track']['artists'][0]['name'])  
                data+= '\n'+str(cont) +' '+ str(j['track']['name']) + ' // '+ str(j['track']['artists'][0]['name'] + ',')   
                
        
          
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    
    D=data.split(',')
   
    return render_template('/ui-spotify.html', mytitle='top 50 canciones más populares', contenido=D)
            
  

# PARA DEVOLVER TWEETS
@app.route("/twitter", methods=['POST'])
def twitter():
    URI_API = 'https://api.twitter.com'


    #ultimos tweets de una busqueda
    tweets_uri = '/2/tweets/search/recent'

    artista = request.form.get("artista")

    '''Buscar un tweets recientes'''
    try:
        parametros = {
            'query' : artista
        }
        header = {
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAC7qaAEAAAAACqCHqNLHGRybM6LTsp252Lo6rjQ%3DzXNnncdySA8L6wsZGu7e6fBfetpFVlwlIzpLAkhUr6upi9DP9S'
        } 
        response = requests.get(URI_API+tweets_uri, headers=header, params=parametros)

    except requests.models.MissingSchema: #pragma: no cover
        raise ServerError('Wrong URL format') from requests.models.MissingSchema

    j = response.content.decode()
    json_data = json.loads(j)
    array_data = json_data['data']
 

    return render_template('/ui-twitter.html', artista=artista, contenido=array_data )

@app.route("/red_social", methods=['POST'])
def redSocial():
    cid = '5ea48a8853c5458b8a8750ab7acf3b63'
    secret = '0469eddbfe5e4543a2b4915f6b3e65c9'
    username = 'najtechnologies'
    redirect_uri = 'http://localhost:8080'
    scope = 'user-top-read'
    token = util.prompt_for_user_token(username,scope,cid,secret,redirect_uri)
    sp = spotipy.Spotify(auth=token)
    playlists=sp.current_user_playlists()
    top='37i9dQZEVXbMDoHDwVN2tF'

    URI_API = 'https://api.twitter.com'
    #ultimos tweets de una busqueda
    tweets_uri = '/2/tweets/search/recent'

    data_spotify = ''
    data_twitter = ''
    cont =0
    while playlists:
        for i, playlist in enumerate(playlists['items']):
       
            tracks=[]
            result = sp.playlist_tracks(top, additional_types=['track'])
        
            tracks  =  result['items']
      
            while result['next']:
                result = sp.next(result)
                tracks.extend(result['items'])

            tweets = []

            for j in tracks:
                cont +=1
                
                parametros = {
                    'query' : str(j['track']['name'])
                }
                header = {
                    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAC7qaAEAAAAACqCHqNLHGRybM6LTsp252Lo6rjQ%3DzXNnncdySA8L6wsZGu7e6fBfetpFVlwlIzpLAkhUr6upi9DP9S'
                } 
                response = requests.get(URI_API+tweets_uri, headers=header, params=parametros)

                y = response.content.decode()
                json_data = json.loads(y)
                data_twitter = json_data['data']
                
                json_grande = []
                for json_algo in data_twitter:
                    json_algo['artist'] = str(j['track']['artists'][0]['name'])
                    json_grande.append(json_algo)

                tweets = tweets + json_grande


                if cont == 3:
                    break

                
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

   
    return render_template('/ui-redsocial.html', contenido=tweets)



# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'
        elif segment == 'register':
            segment = 'login'
        elif segment == 'login':
            segment = 'index'

        return segment    

    except:
        return None

    #Cargamos 2 datasets
iris = data('iris')
tips = data('tips')

# grafica % tweets positivos

tweets = np.linspace(0,60,256, endpoint = True)
#c, s = np.tweets, np.canciones

#tamaño figura
plt.figure(figsize=(8,6))
plt.plot(x,c, color = "blue", linewidth = 2.5, linestyle="-", label ="tweets")
plt.plot(x,s, color = "green", linewidth = 2.5, linestyle="-", label ="canciones")

#personalizando valores de los ejes
plt.xticks([0,10,20,30,40,50],[r'$ +\0 $', r'$+\10$', r'$+\20$', r'$+\30$', r'$+\40$',r'$+\50$']])
plt.yticks([0,+1],[r'$0$', r'$+1$'])
plt.legend(loc='upper left')

ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.spines['bottom'].set_position(('data',0))
ax.yaxis.set_ticks_position(('left'))
ax.spines['left'].set_position(('data',0))

plt.show()
#histograma
iris.head()

#twitter y spotify
twitter = iris[iris.Species == 'tweets']
spotify = iris[iris.Species == 'canciones']

plt.figure(figsize=(10, 8))
n, bins, patches = plt.hist(twitter['Petal.Length'], 12, facecolor='blue', label='tweets')
n, bins, patches = plt.hist(spotify['Petal.Length'], 12, facecolor='green', label='canciones')

plt.legend(loc='top_right')
plt.title('Histograma largo de los tweets')
plt.xlabel('largo del tweet')
plt.ylabel('cuenta largo del tweet')
plt.show()
