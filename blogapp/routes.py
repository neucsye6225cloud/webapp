from flask import request, make_response, jsonify
from pymysql import IntegrityError
from blogapp import app, db, basic_auth
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from blogapp.models import User
from flask_login import login_user, current_user
import logging

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

    return make_response('')


@app.errorhandler(405)
def handle_http_errors(error):
    response = make_response('')
    response.headers['Cache-Control'] = 'no-cache'
    return response, 405
