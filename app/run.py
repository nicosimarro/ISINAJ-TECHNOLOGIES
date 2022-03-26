# -*- encoding: utf-8 -*-
"""
NAJ-Technologies
"""


# import Flask 
# Flask modules
from flask   import render_template, request
from jinja2  import TemplateNotFound

from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

import jwt
from datetime import datetime, timedelta

# Inject Flask magic
app = Flask(__name__)

# App Config - the minimal footprint
app.config['TESTING'   ] = True 
app.config['SECRET_KEY'] = 'S#perS3crEt_JamesBond'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/julian/integracion/jinja-black-dashboard_v2/jinja-black-dashboard/usuarios.db'
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
