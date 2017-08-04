from flask import jsonify
from validate_email import validate_email
from modals.modals import UserModal


class Authenticate(object):
    """
    Handles all user operations
    """

    @staticmethod
    def register(email, password, name):
        """
        Registers a new user to the application
        and returns an API response with status
        code set to 201 on success
        
        :param email: 
        :param password: 
        :param name:  
        """
        if not name or not email or not password:
            response = jsonify({'Error': 'Missing Values'})
            response.status_code = 400
            return response

        if not validate_email(email):
            response = jsonify({'Error': 'Invalid Email'})
            response.status_code = 400
            return response

        if len(password) < 6:
            response = jsonify({'Error': 'Password is short'})
            response.status_code = 400
            return response

        user = UserModal(email=email, password=password, name=name)

        if user.query.filter_by(email=email).first():
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

    @staticmethod
    def login(email, password):
        """
        logs in an existing user to the application
        and returns an API response with status
        code set to 201 on success
        
        :param email: 
        :param password:  
        """
        if not email or not password:
            response = jsonify({'Error': 'Missing login credentials'})
            response.status_code = 400
            return response

        if not validate_email(email):
            response = jsonify({'Error': 'Enter valid email'})
            response.status_code = 400
            return response

        user = UserModal(email=email, password=password)
        user_data = user.query.filter_by(email=email).first()

        # If Login successful
        if user_data and user.check_password(user_data.password,
                                             password):
            response = jsonify({
                'Status': user.email + ' Login Successful',
                'id': user_data.id
            })
            response.status_code = 201
            return response

        response = jsonify({'Error': 'Incorrect email or password'})
        response.status_code = 400
        return response

    @staticmethod
    def reset_password(email):
        """
        resets password of an existing user
        and returns an API response with status
        code set to 201 on success
        
        :param email:  
        """
        if not email:
            response = jsonify({'Error': 'No email sent'})
            response.status_code = 400
            return response

        if not validate_email(email):
            response = jsonify({'Error': 'Enter valid email'})
            response.status_code = 400
            return response

        user = UserModal(email=email, password='')
        user_data = user.query.filter_by(email=email).first()
        if user_data:
            return 0
        response = jsonify({'Error': 'Email does not exist'})
        response.status_code = 400
        return response
