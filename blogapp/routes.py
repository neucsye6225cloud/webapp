import base64
from flask import request, make_response, jsonify
from blogapp import app, db, bcrypt, auth
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from blogapp.models import User
import logging
from datetime import datetime

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)

@auth.verify_password
def verify_password(username, password):

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

@app.route('/healthz', methods=['GET', 'HEAD', 'OPTIONS'])
def health_check():

    if request.method in ['HEAD', 'OPTIONS']:
        return make_response(''), 405

    if request.get_data():
        return make_response(''), 400

    try:
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return make_response('', 200)
    
    except SQLAlchemyError as e:
        return make_response(''), 503

@app.route('/v1/user', methods=['POST'])
def create_user():

    # check for syntax error in json request body
    try:
        data = request.get_json()
    except (ValueError, KeyError, TypeError):
        return make_response(''), 400
    
    # validation for mandatory fields
    required_fields = ['first_name', 'last_name', 'password', 'username'] 
    updated_fields = [field for field in required_fields if field in data]
    if len(updated_fields) != len(data):
        return make_response(''), 400

    try:
        # validation of email address already exists for the user
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user:
            return make_response(''), 400

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

        return make_response(jsonify(response_payload), 201)

    except IntegrityError as e:
        # database integrity 
        db.session.rollback()
        return make_response(jsonify({'error': 'Database integrity error'}), 503)
    except (ValueError, KeyError, TypeError):
        db.session.rollback()
        return make_response('', 400)

@app.route('/v1/user/self', methods=['GET'])
@auth.login_required
def get_user():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return make_response('', 401)
    
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
        return make_response('', 404)

    return make_response('', 401)

@app.route('/v1/user/self', methods=['PUT'])
@auth.login_required
def update_user_info():

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return make_response('', 401)

    try:
        data = request.get_json()
    except (ValueError, KeyError, TypeError):
        return make_response(''), 400

    try:
        auth_type, credentials = auth_header.split(' ')
        if auth_type.lower() == 'basic':
            decoded_credentials = base64.b64decode(credentials).decode('utf-8')
            username, _ = decoded_credentials.split(':', 1)

            user = User.query.filter_by(username=username).first()
            if not user:
                return make_response(jsonify({'error': 'User not found'}), 404)

        # Check if only allowed fields are being updated
        allowed_fields = ['first_name', 'last_name', 'password']
        updated_fields = [field for field in allowed_fields if field in data]
        if len(updated_fields) != len(data):
            return make_response(jsonify({'error': 'Invalid fields for update'}), 400)

        # Update user information
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        # user.password = bcrypt.generate_password_hash(data.get('password', user._password)).decode('utf-8')
        password_update = data.get('password', user._password)

        # Only update the password if a new one is provided
        if password_update != user._password:
            user.password = bcrypt.generate_password_hash(password_update).decode('utf-8')


        # Save the updated user to the database
        db.session.commit()

        # Response payload without password
        response_payload = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "account_created": user.account_created.isoformat()
        }

        return make_response('', 204)
    except IntegrityError as e:
        # database integrity 
        db.session.rollback()
        return make_response(jsonify({'error': 'Database integrity error'}), 503) 


@app.errorhandler(405)
def method_not_allowed(error):
    return make_response(''), 405

@auth.error_handler
def authorized_access():
    return make_response(''), 401
