import unittest
from flask import json
from api import db
from api.BucketListAPI import app
from instance.config import application_config


class BucketTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(application_config['TestingEnv'])
        self.client = app.test_client()

        # Binds the app to current context
        with app.app_context():
            # Create all tables
            db.create_all()

        user = json.dumps({
            'email': 'pat@gmail.com',
            'password': 'bucketlist',
            'name': 'Patrick'
        })
        response = self.client.post('/auth/register', data=user)
        json_repr = json.loads(response.data.decode())
        self.token = json_repr['id']

    def test_add_bucket_without_bucket_name(self):
        """Should return 400 for missing bucket name"""
        bucket = json.dumps({
            'bucket': '',
            'desc': 'travel'
        })
        response = self.client.post('/auth/bucket', data=bucket,
                                    headers={"Authorization" : self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing', response.data.decode())

    def test_add_bucket_successfully(self):
        """Should return 201 for bucket added"""
        bucket = json.dumps({
            'bucket': 'Travel',
            'desc': 'Visit places'
        })
        response = self.client.post('/auth/bucket', data=bucket,
                                    headers={"Authorization" : self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully', response.data.decode())

    def tearDown(self):
        # Drop all tables
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
