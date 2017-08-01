from flask import jsonify, request
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
        return user.register()


    except KeyError:
        response = jsonify({'Error': 'Invalid Keys detected'})
        response.status_code = 500
        return response


if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug=True)
