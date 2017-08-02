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
        response = self.client.post('/bucket', data=bucket,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing', response.data.decode())

    def test_add_bucket_successfully(self):
        """Should return 201 for bucket added"""
        bucket = json.dumps({
            'bucket': 'Travel',
            'desc': 'Visit places'
        })
        response = self.client.post('/bucket', data=bucket,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully', response.data.decode())

    def test_add_bucket_with_existing_bucket_name(self):
        """Should return 400 for missing bucket name"""

        # First Add bucket
        self.test_add_bucket_successfully()
        bucket = json.dumps({
            'bucket': 'Travel',
            'desc': 'travel'
        })
        response = self.client.post('/bucket', data=bucket,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Bucket name Already exists', response.data.decode())

    def test_get_bucket_when_DB_is_empty(self):
        """Should return all buckets lists"""
        response = self.client.get('/buckets',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('No bucketlist has been created',
                      response.data.decode())

    def test_get_bucket(self):
        """Should return all buckets lists"""

        # First add bucket
        self.test_add_bucket_successfully()
        response = self.client.get('/buckets',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Travel',
                      response.data.decode())

    def test_get_bucket_search(self):
        """Should return all buckets lists"""

        # First add bucket
        self.test_add_bucket_successfully()
        response = self.client.get('/buckets?q=Travel',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Travel',
                      response.data.decode())

    def test_get_single_bucket(self):
        """Should return all buckets lists"""

        # First add bucket
        self.test_add_bucket_successfully()
        response = self.client.get('/buckets/1',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Travel',
                      response.data.decode())

    def test_get_single_bucket_with_no_bucket(self):
        """Should return all buckets lists"""

        response = self.client.get('/buckets/1',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('No bucketlist',
                      response.data.decode())

    def test_get_single_bucket_not_existing(self):
        """Should return all buckets lists"""

        # First add bucket
        self.test_add_bucket_successfully()
        response = self.client.get('/buckets/2',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('bucketlist with id 2 not found',
                      response.data.decode())

    def test_get_single(self):
        """Should return all buckets lists"""

        # First add bucket
        self.test_add_bucket_successfully()
        response = self.client.get('/buckets/1',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Travel',
                      response.data.decode())

    def tearDown(self):
        # Drop all tables
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
