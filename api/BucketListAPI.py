import datetime

import jwt
from flask import jsonify, request, json
from api import create_app
from classes.authenticate import Authenticate
from classes.bucket import Bucket

app = create_app('DevelopmentEnv')


@app.route('/')
def index():
    """Index route"""
    response = jsonify({'Welcome Message': 'Hello'})
    response.status_code = 201
    return response


@app.route('/auth/register', methods=['POST'])
def register():
    """Route to handle user registration"""
    request.get_json(force=True)
    try:
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        user = Authenticate()
        response = user.register(email, password, name)
        if response.status_code == 201:
            data = json.loads(response.data.decode())
            data['id'] = encode_auth_token(data['id']).decode()
            response = jsonify(data)
            response.status_code = 201
        return response

    except KeyError:
        response = jsonify({'Error': 'Invalid Keys detected'})
        response.status_code = 500
        return response


@app.route('/auth/login', methods=['POST'])
def login():
    """Route to handle user login"""
    request.get_json(force=True)
    try:
        email = request.json['email']
        password = request.json['password']
        user = Authenticate()
        response = user.login(email, password)
        if response.status_code == 201:
            data = json.loads(response.data.decode())
            data['id'] = encode_auth_token(data['id']).decode()
            response = jsonify(data)
            response.status_code = 201
        return response

    except KeyError:
        response = jsonify({'Error': 'Invalid Keys detected'})
        response.status_code = 500
        return response


@app.route('/auth/reset-password', methods=['POST'])
def reset_password():
    """Route to handle reset password"""
    request.get_json(force=True)
    try:
        email = request.json['email']
        user = Authenticate()
        response = user.reset_password(email)
        return response

    except KeyError:
        response = jsonify({'Error': 'Invalid Keys detected'})
        response.status_code = 500
        return response


@app.route('/auth/bucket', methods=['POST'])
def add_bucket():
    """Route to handle creating a bucket"""
    request.get_json(force=True)
    try:
        token = request.headers.get("Authorization")
        user_id = decode_auth_token(token)
        if isinstance(user_id, int):
            bucket_name = request.json['bucket']
            desc = request.json['desc']
            bucket = Bucket()
            response = bucket.create_bucket(bucket_name, desc, user_id)
            return response

    except KeyError:
        response = jsonify({'Error': 'Invalid Keys detected'})
        response.status_code = 500
        return response


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() +
                   datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
        return payload['sub']
    except jwt.ExpiredSignatureError:
        response = jsonify({
            'Expired': 'Signature expired. Please log in again.'
        })
        response.status_code = 401
        return response

    except jwt.InvalidTokenError:
        response = jsonify({
            'Invalid': 'Invalid token. Please log in again.'
        })
        response.status_code = 401
        return response


if __name__ == '__main__':
    app.run()
