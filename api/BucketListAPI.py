from flask import Flask, jsonify, request
from modals.modals import User, Bucket, Item
from api import create_app, db
from validate_email import validate_email
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

        if not name or not email or not password:
            response = jsonify({'Error': 'Missing Values'})
            response.status_code = 400
            return response

        if not validate_email(email):
            response = jsonify({'Error': 'Invalid Email'})
            response.status_code = 400
            return response

    except KeyError:
        response = jsonify({'Error': 'Invalid Keys detected'})
        response.status_code = 500
        return response


if __name__ == '__main__':
    app.run()
