from flask import Flask, jsonify, request
from modals.modals import User, Bucket, Item
from api import create_app, db

app = create_app('DevelopmentEnv')


@app.route('/')
def index():
    response = jsonify({'Welcome Message': 'Hello'})
    response.status_code = 201
    return response



if __name__ == '__main__':
    app.run()
