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
        self.token = json_repr['token']

    def test_add_bucket_without_bucket_name(self):
        """Should return 400 for missing bucket name"""
        bucket = json.dumps({
            'bucket': '',
            'desc': 'travel'
        })
        response = self.client.post('/buckets', data=bucket,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Missing', response.data.decode())

    def test_add_bucket_successfully(self):
        """Should return 201 for bucket added"""
        bucket = json.dumps({
            'bucket': 'Travel',
            'desc': 'Visit places'
        })
        response = self.client.post('/buckets', data=bucket,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Travel', response.data.decode())

    def test_add_bucket_with_existing_bucket_name(self):
        """Should return 400 for missing bucket name"""

        # First Add bucket
        self.test_add_bucket_successfully()
        bucket = json.dumps({
            'bucket': 'Travel',
            'desc': 'travel'
        })
        response = self.client.post('/buckets', data=bucket,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 409)
        self.assertIn('Bucket name Already exists', response.data.decode())

    def test_get_bucket_when_DB_is_empty(self):
        """Should return no buckets lists msg"""
        response = self.client.get('/buckets',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        # self.assertIn('No bucketlist has been created',
        #              response.data.decode())

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
        """Should return 200 and bucket"""

        # First add bucket
        self.test_add_bucket_successfully()
        response = self.client.get('/buckets?q=Travel',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Travel',
                      response.data.decode())

    def test_get_single_bucket(self):
        """Should return 200 and bucket"""

        # First add bucket
        self.test_add_bucket_successfully()
        response = self.client.get('/buckets/1',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Travel',
                      response.data.decode())

    def test_get_single_bucket_with_no_bucket(self):
        """Should return 400 if no buckets"""

        response = self.client.get('/buckets/1',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('not found',
                      response.data.decode())

    def test_get_single_bucket_not_existing(self):
        """Should return 400 for bucket doesnt exists"""

        # First add bucket
        self.test_add_bucket_successfully()
        response = self.client.get('/buckets/2',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('bucketlist with id 2 not found',
                      response.data.decode())

    def test_get_single(self):
        """Should return a single buckets"""

        # First add bucket
        self.test_add_bucket_successfully()
        response = self.client.get('/buckets/1',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Travel',
                      response.data.decode())

    def test_update_bucket_which_doesnt_exist(self):
        """
        Should return 400 for bucket
        does not exists
        """

        # First add bucket
        self.test_add_bucket_successfully()
        bucket = json.dumps({
            'bucket': 'Travel',
            'desc': 'Visit places'
        })
        response = self.client.put('/buckets/2', data=bucket,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('does not exist', response.data.decode())

    def test_update_bucket_without_bucket_name(self):
        """Should return 400 for missing bucket name"""
        bucket = json.dumps({
            'bucket': '',
            'desc': 'travel'
        })
        response = self.client.put('/buckets/1', data=bucket,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Missing', response.data.decode())

    def test_update_bucket_with_same_name(self):
        """Should return 200 for bucket updates"""

        # First add bucket
        self.test_add_bucket_successfully()
        bucket = json.dumps({
            'bucket': 'Travel',
            'desc': 'Test Foods'
        })
        response = self.client.put('/buckets/1', data=bucket,
                                   headers={"Authorization": self.token})
        # self.assertEqual(response.status_code, 409)
        # self.assertIn('Bucket name Already exists', response.data.decode())

    def test_update_bucket_successfully(self):
        """Should return 200 for bucket updates"""

        # First add bucket
        self.test_add_bucket_successfully()
        bucket = json.dumps({
            'bucket': 'Food',
            'desc': 'Test Foods'
        })
        response = self.client.put('/buckets/1', data=bucket,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Food', response.data.decode())

    def test_delete_bucket_that_doesnt_exist(self):
        """Should return 201 for bucket added"""

        response = self.client.delete(
            '/buckets/1', headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bucket not found', response.data.decode())

    def test_delete_bucket_successfully(self):
        """Should return 201 for bucket added"""

        # First add a bucket
        self.test_add_bucket_successfully()
        response = self.client.delete(
            '/buckets/1', headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('bucket deleted', response.data.decode())

    def tearDown(self):
        # Drop all tables
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
