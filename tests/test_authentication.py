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

    def tearDown(self):
        # Drop all tables
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
