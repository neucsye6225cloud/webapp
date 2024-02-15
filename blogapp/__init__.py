from flask_bcrypt import Bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_httpauth import HTTPBasicAuth 
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/cloud'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BCRYPT_HANDLE_LONG_PASSWORDS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
auth = HTTPBasicAuth()

# to avoid circular recursive imports and import error, import routes after creating app, db objects 
from blogapp import routes

with app.app_context():
    db.create_all()

@app.after_request
def add_security_headers(response):
    response.headers['Cache-Control'] = 'no-cache'
    return response
