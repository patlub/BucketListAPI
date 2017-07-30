from flask import Flask, jsonify
from modals.modals import User, Bucket, Item
from api.__init__ import create_app, db

app = create_app('DevelopmentEnv')


@app.errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'The request can not be completed'})
    response.status_code = 404
    return response

@app.errorhandler(401)
def invalid_token(e):
    response = jsonify({'error': 'Invalid Token'})
    response.status_code = 401
    return response


if __name__ == '__main__':
    app.run()
