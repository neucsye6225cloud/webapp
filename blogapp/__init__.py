from flask_bcrypt import Bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_httpauth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import logging.config
from pythonjsonlogger import jsonlogger

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv("/tmp/webapp/webapp.env")
db_name = os.getenv("DB_NAME", "cloud")
db_user = os.getenv("DB_USER", "root")
db_password = os.getenv("DB_PASSWORD", "root")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "3306")
project_id = os.getenv("PROJECT_ID")
instance_name = os.getenv("SQL_INSTANCE")

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BCRYPT_HANDLE_LONG_PASSWORDS'] = True


# Configure logging to write structured logs in JSON
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
        }
    },
    'handlers': {
        # 'wsgi': {
        #     'class': 'logging.StreamHandler',
        #     'formatter': 'json',
        #     'stream': 'ext://sys.stdout'
        # },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'filename': '/var/log/blogapp/myapp.log',
            'formatter': 'json',
            'maxBytes': 5 * 1024 * 1024,
        }
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['file']
        }
    }
})

# custom JSON log formatter for the Flask app logger
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
app.logger.addHandler(handler)


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
