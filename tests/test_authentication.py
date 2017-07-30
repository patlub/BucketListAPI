import unittest
from flask import json
from api import create_app, db


class AuthenticationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name='TestingEnv')
        self.client = self.app.test_client()

        # Binds the app to current context
        with self.app.app_context():
            # Create all tables
            db.create_all()

    def tearDown(self):
        # Drop all tables
        with self.app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()

    def test_something(self):
        self.assertTrue(1)


if __name__ == '__main__':
    unittest.main()
