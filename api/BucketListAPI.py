import datetime

import jwt
from flask import jsonify, request, json
from api import create_app
from classes.user import User

app = create_app('DevelopmentEnv')


@app.route('/')
def index():
    response = jsonify({'Welcome Message': 'Hello'})
    response.status_code = 201
    return response


@app.route('/auth/register', methods=['POST'])
def register():
    request.get_json(force=True)
    try:
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        user = User(email, password, name)
        response = user.register()
        if response.status_code == 201:
            user_id = json.loads(response.data.decode())['id']
            encode_auth_token(user_id)
        return response

    except KeyError:
        response = jsonify({'Error': 'Invalid Keys detected'})
        response.status_code = 500
        return response

@app.route('/auth/login', methods=['POST'])
def login():
    request.get_json(force=True)
    try:
        email = request.json['email']
        password = request.json['password']
        user = User(email, password)
        response = user.login()
        if response.status_code == 201:
            user_id = json.loads(response.data.decode())['id']
            encode_auth_token(user_id)
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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
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


if __name__ == '__main__':
    app.run()
