import unittest

from flask import json

from api.__init__ import app, Env_name, db


class AuthenticationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        Env_name('TestingEnv')
        db.create_all()

    def tearDown(self):
        pass
        db.session.remove()
        db.drop_all()

    def test_unavailable_request(self):
        data = json.dumps({'username': 'patrick', 'password': 'secret'})
        response = self.app.post()
        # self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
