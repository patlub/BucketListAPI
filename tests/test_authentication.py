import unittest
from flask import json
from api import db
from api.BucketListAPI import app
from instance.config import application_config


class AuthenticationTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(application_config['TestingEnv'])
        self.client = app.test_client()

        # Binds the app to current context
        with app.app_context():
            # Create all tables
            db.create_all()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Welcome Message', response.data.decode())

    def test_registration_with_missing_dredentials(self):
        """Should throw error for missing credentials"""
        user = json.dumps({
            'name': '',
            'email': '',
            'password': ''
        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing', response.data.decode())

    def test_registration_with_invalid_email(self):
        """Should return invalid email"""
        user = json.dumps({
            'name': 'Patrick',
            'email': 'pato',
            'password': 'patrick'
        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid Email', response.data.decode())

    def test_registration_with_short_password(self):
        """Should return invalid email"""
        user = json.dumps({
            'name': 'Patrick',
            'email': 'pato@gmail.com',
            'password': 'pato'
        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Password is short', response.data.decode())

    def test_for_existing_email(self):
        """Should check if email exists"""
        user = json.dumps({
            'name': 'Patrick',
            'email': 'pato@gmail.com',
            'password': 'patrickluboobi'
        })
        self.client.post('/auth/register', data=user)
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Email Already exists', response.data.decode())

    def test_successfull_registration(self):
        """Should register user successfully"""
        user = json.dumps({
            'name': 'Patrick',
            'email': 'pato@gmail.com',
            'password': 'patrickluboobi'
        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully registered', response.data.decode())


    def tearDown(self):
        # Drop all tables
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
