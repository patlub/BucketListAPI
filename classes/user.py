from flask import jsonify
from validate_email import validate_email
from modals.modals import UserModal


class User(object):
    """
    Handles all user operations
    """

    def __init__(self, email, password, name=None):
        self.email = email
        self.name = name
        self.password = password

    def register(self):
        """
        Registers a new user to the application
        and returns an API response with status
        code set to 201 on success
        """
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
            'Status': user.email + ' Successfully registered',
            'id': user.id
        })
        response.status_code = 201
        return response

    def login(self):
        """
        logs in an existing user to the application
        and returns an API response with status
        code set to 201 on success
        """
        if not self.email or not self.password:
            response = jsonify({'Error': 'Missing login credentials'})
            response.status_code = 400
            return response

        if not validate_email(self.email):
            response = jsonify({'Error': 'Enter valid email'})
            response.status_code = 400
            return response

        user = UserModal(email=self.email, password=self.password)
        user_data = user.query.filter_by(email=self.email).first()

        # If Login successful
        if user_data and user.check_password(user_data.password,
                                             self.password):
            response = jsonify({
                'Status': user.email + ' Login Successful',
                'id': user.id
            })
            response.status_code = 201
            return response

        response = jsonify({'Error': 'Incorrect email or password'})
        response.status_code = 400
        return response
