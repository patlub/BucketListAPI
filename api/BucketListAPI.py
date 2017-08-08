import datetime

import jwt
from flask import jsonify, request, json, render_template
from api import create_app
from classes.authenticate import Authenticate
from classes.bucket import Bucket
from classes.item import Item

app = create_app('ProductionEnv')


@app.route('/', methods=['GET'])
def index():
    """Index route"""
    return render_template('index.html')


@app.route('/auth/register', methods=['POST'])
def register():
    """Method to handle user registration"""
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
    """Method to handle user login"""
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
    """Method to handle reset password"""
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


@app.route('/buckets', methods=['POST'])
def add_bucket():
    """Method to handle creating a bucket"""
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
        response = jsonify({'Error': 'Invalid Token'})
        response.status_code = 400
        return response

    except KeyError:
        response = jsonify({'Error': 'Invalid Keys detected'})
        response.status_code = 500
        return response


@app.route('/buckets', methods=['GET'])
def get_buckets():
    """Method to handle getting all buckets"""
    try:
        token = request.headers.get("Authorization")
        data = decode_auth_token(token)
        if isinstance(data, int):
            user_id = data
            search = request.args.get("q", "")
            bucket = Bucket()
            response = bucket.get_buckets(user_id, search)
            return response
        else:
            response = jsonify({'Error': 'Invalid Token'})
            response.status_code = 400
            return response

    except KeyError:
        response = jsonify({'Error': 'Invalid Keys detected'})
        response.status_code = 500
        return response


@app.route('/buckets/<int:bucket_id>', methods=['GET'])
def get_single_bucket(bucket_id):
    """Method to handle getting a single bucket"""
    try:
        token = request.headers.get("Authorization")
        data = decode_auth_token(token)
        if isinstance(data, int):
            user_id = data
            bucket = Bucket()
            response = bucket.get_single_bucket(user_id, bucket_id)
            return response
        else:
            response = jsonify({'Error': 'Invalid Token'})
            response.status_code = 400
            return response

    except KeyError:
        response = jsonify({'Error': 'Invalid Keys detected'})
        response.status_code = 500
        return response


@app.route('/buckets/<int:bucket_id>', methods=['PUT'])
def update_bucket(bucket_id):
    """Method to handle updating a bucket"""
    request.get_json(force=True)
    try:
        token = request.headers.get("Authorization")
        data = decode_auth_token(token)
        if isinstance(data, int):
            bucket_name = request.json['bucket']
            desc = request.json['desc']
            user_id = data
            bucket = Bucket()
            response = bucket.update_bucket(user_id, bucket_id,
                                            bucket_name, desc)
            return response
        else:
            response = jsonify({'Error': 'Invalid Token'})
            response.status_code = 400
            return response

    except KeyError:
        response = jsonify({'Error': 'Invalid Keys detected'})
        response.status_code = 500
        return response


@app.route('/buckets/<int:bucket_id>', methods=['DELETE'])
def delete_bucket(bucket_id):
    """Method to handle creating a bucket"""
    try:
        token = request.headers.get("Authorization")
        data = decode_auth_token(token)
        if isinstance(data, int):
            user_id = data
            bucket = Bucket()
            response = bucket.delete_bucket(user_id, bucket_id)
            return response
        else:
            response = jsonify({'Error': 'Invalid Token'})
            response.status_code = 400
            return response

    except KeyError:
        response = jsonify({'Error': 'Invalid Keys detected'})
        response.status_code = 500
        return response


@app.route('/buckets/<int:bucket_id>/items', methods=['POST'])
def add_item(bucket_id):
    """Method to handle creating a bucket"""
    request.get_json(force=True)
    try:
        token = request.headers.get("Authorization")
        data = decode_auth_token(token)
        if isinstance(data, int):
            item_name = request.json['item']
            user_id = data
            item = Item()
            response = item.add_item(user_id, bucket_id, item_name)
            return response
        else:
            response = jsonify({'Error': 'Invalid Token'})
            response.status_code = 400
            return response

    except KeyError:
        response = jsonify({'Error': 'Invalid Keys detected'})
        response.status_code = 500
        return response


@app.route('/buckets/<int:bucket_id>/items/<int:item_id>', methods=['PUT'])
def edit_item(bucket_id, item_id):
    """Method to handle creating a bucket"""
    request.get_json(force=True)
    try:
        token = request.headers.get("Authorization")
        data = decode_auth_token(token)
        if isinstance(data, int):
            item_name = request.json['item']
            user_id = data
            item = Item()
            response = item.edit_item(user_id, bucket_id, item_id, item_name)
            return response
        else:
            response = jsonify({'Error': 'Invalid Token'})
            response.status_code = 400
            return response

    except KeyError:
        response = jsonify({'Error': 'Invalid Keys detected'})
        response.status_code = 500
        return response


@app.route('/buckets/<int:bucket_id>/items/<int:item_id>', methods=['DELETE'])
def delete_item(bucket_id, item_id):
    """Method to handle creating a bucket"""
    try:
        token = request.headers.get("Authorization")
        data = decode_auth_token(token)
        if isinstance(data, int):
            user_id = data
            item = Item()
            response = item.delete_item(user_id, item_id)
            return response
        else:
            response = jsonify({'Error': 'Invalid Token'})
            response.status_code = 400
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
                   datetime.timedelta(days=0, seconds=3600),
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
