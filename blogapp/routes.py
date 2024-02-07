import base64
from flask import request, make_response, jsonify
from blogapp import app, db, basic_auth, bcrypt
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from blogapp.models import User
# from flask_login import login_user, current_user
import logging
from datetime import datetime

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

@app.route('/healthz', methods=['GET', 'HEAD', 'OPTIONS'])
def health_check():

    if request.method in ['HEAD', 'OPTIONS']:
        response = make_response('')
        response.headers['Cache-Control'] = 'no-cache'
        return response, 405

    if request.get_data():
        response = make_response('')
        response.headers['Cache-Control'] = 'no-cache'
        return response, 400

    try:
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        response = make_response('')
        response.headers['Cache-Control'] = 'no-cache'
        return response
    
    except SQLAlchemyError as e:
        response = make_response('')
        response.headers['Cache-Control'] = 'no-cache'
        return response, 503

@app.route('/v1/user', methods=['POST'])
def create_user():

    # check for syntax error in json request body
    try:
        data = request.get_json()
    except (ValueError, KeyError, TypeError):
        return make_response(''), 400

    # validation for mandatory fields
    required_fields = ['first_name', 'last_name', 'password', 'username']
    if not all(field in data for field in required_fields):
        response = make_response('')
        response.headers['Cache-Control'] = 'no-cache'
        return response, 400

    try:
        # validation of email address already exists for the user
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            response = make_response('')
            response.headers['Cache-Control'] = 'no-cache'
            return response, 400

        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=data['password'],
            username=data['username']
        )

        # Save the new user to the database
        db.session.add(new_user)
        db.session.commit()

        response_payload = {
            "id": new_user.id,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "username": new_user.username,
            "account_created": new_user.account_created.isoformat(),
            "account_updated": new_user.account_updated.isoformat()
        }

        # # Response headers
        # response_headers = {
        #     'access-control-allow-credentials': 'true',
        #     'access-control-allow-headers': 'X-Requested-With,Content-Type,Accept,Origin',
        #     'access-control-allow-methods': '*',
        #     'access-control-allow-origin': '*',
        #     'cache-control': 'no-cache',
        #     'content-encoding': 'gzip',
        #     'content-type': 'application/json;charset=utf-8',
        #     'date': datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
        #     'expires': '-1',
        #     'server': 'nginx',
        #     'x-powered-by': 'Express'
        # }

        return make_response(jsonify(response_payload), 201)

    except IntegrityError as e:
        # database integrity 
        db.session.rollback()
        return make_response(jsonify({'error': 'Database integrity error'}), 500)

@app.route('/v1/user/self', methods=['GET'])
@basic_auth.required
def get_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return make_response(jsonify({'error': 'Authorization header missing'}), 401)
    
    try:
        auth_type, credentials = auth_header.split(' ')
        if auth_type.lower() == 'basic':
            decoded_credentials = base64.b64decode(credentials).decode('utf-8')
            username, _ = decoded_credentials.split(':', 1)

            user = User.query.filter_by(username=username).first()
            if not user:
                return make_response(jsonify({'error': 'User not found'}), 404)
            
            response_payload = {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "account_created": user.account_created.isoformat(),
                "account_updated": user.account_updated.isoformat()
            }

        return make_response(jsonify(response_payload), 200)

    except ValueError:
        pass

    return make_response(jsonify({'error': 'Invalid Authorization header'}), 401)

@app.route('/v1/user/self', methods=['PUT'])
@basic_auth.required
def update_user_info():

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return make_response(jsonify({'error': 'Authorization header missing'}), 401)

    auth_type, credentials = auth_header.split(' ')
    if auth_type.lower() == 'basic':
        decoded_credentials = base64.b64decode(credentials).decode('utf-8')
        username, _ = decoded_credentials.split(':', 1)

        user = User.query.filter_by(username=username).first()
        if not user:
            return make_response(jsonify({'error': 'User not found'}), 404)
        
    data = request.get_json()

    # except (ValueError, KeyError, TypeError):
    #     return make_response(''), 400

    # Check if only allowed fields are being updated
    allowed_fields = ['first_name', 'last_name', 'password']
    if not all(field in data for field in allowed_fields) or len(data) != len(allowed_fields):
        return make_response(jsonify({'error': 'Invalid fields for update'}), 400)

    # Update user information
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.password = bcrypt.generate_password_hash(data.get('password', user._password)).decode('utf-8')
    user.account_updated = datetime.utcnow()

    # Save the updated user to the database
    db.session.commit()

    # Response payload without password
    response_payload = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "account_created": user.account_created.isoformat(),
        "account_updated": user.account_updated.isoformat()
    }

    # # Response headers
    # response_headers = {
    #     'access-control-allow-credentials': 'true',
    #     'access-control-allow-headers': 'X-Requested-With,Content-Type,Accept,Origin',
    #     'access-control-allow-methods': '*',
    #     'access-control-allow-origin': '*',
    #     'cache-control': 'no-cache',
    #     'content-encoding': 'gzip',
    #     'content-type': 'application/json;charset=utf-8',
    #     'date': datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
    #     'expires': '-1',
    #     'server': 'nginx',
    #     'x-powered-by': 'Express'
    # }

    return make_response('', 204)



@app.errorhandler(405)
def handle_http_errors(error):
    response = make_response('')
    response.headers['Cache-Control'] = 'no-cache'
    return response, 405
