from flask import request, jsonify
from validate_email import validate_email

from modals.modals import UserModal


class User(object):
    def __init__(self, email, password, name=None):
        self.email = email
        self.name = name
        self.password = password

    def register(self):

        if not self.name or not self.email or not self.password:
            response = jsonify({'Error': 'Missing Values'})
            response.status_code = 400
            return response

        if not validate_email(self.email):
            response = jsonify({'Error': 'Invalid Email'})
            response.status_code = 400
            return response

        if len(self.password) < 6:
            response = jsonify({'Error': 'Password is short'})
            response.status_code = 400
            return response

        user = UserModal(email=self.email, password=self.password, name=self.name)

        if user.query.filter_by(email=self.email).first():
            response = jsonify({'Error': 'Email Already exists'})
            response.status_code = 400
            return response

        user.save()
        response = jsonify({
            'Status': user.email + ' Successfully registered'
        })
        response.status_code = 201
        return response
