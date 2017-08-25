import unittest
from flask import json
from api import db
from api.BucketListAPI import app
from instance.config import application_config


class ItemTestCase(unittest.TestCase):
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

    def test_add_item_with_no_name(self):
        """Should return 400 for missing item name"""
        item = json.dumps({'item': ''})
        response = self.client.post('/buckets/1/items', data=item,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Missing Item name', response.data.decode())

    def test_add_item_when_bucket_doesnt_exist(self):
        """Should return 400 for missing bucket"""
        item = json.dumps({'item': 'Go to Nairobi'})
        response = self.client.post('/buckets/1/items', data=item,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bucket with id 1 not found', response.data.decode())

    def test_add_item_successfully(self):
        """Should return 201 for item added"""

        # First add the bucket
        bucket = json.dumps({
            'bucket': 'Travel',
            'desc': 'Visit places'
        })
        self.client.post('/buckets', data=bucket,
                         headers={"Authorization": self.token})

        item = json.dumps({'item': 'Go to Nairobi'})
        response = self.client.post('/buckets/1/items', data=item,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Go to Nairobi', response.data.decode())

    def test_get_items_when_DB_empty(self):
        """Should return no items msg"""

        response = self.client.get('/items/1',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('No item has been created',
                      response.data.decode())

    def test_get_items(self):
        """Should return all buckets items"""

        # First add item
        self.test_add_item_successfully()
        response = self.client.get('/items/1',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Go to Nairobi',
                      response.data.decode())

    def test_add_duplicate_item(self):
        """Should return 400 for duplicate item"""

        # First add the item
        self.test_add_item_successfully()
        item = json.dumps({'item': 'Go to Nairobi'})
        response = self.client.post('/buckets/1/items', data=item,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('item name Already exists', response.data.decode())

    def test_edit_item_with_no_name(self):
        """Should return 400 for missing item name"""

        item = json.dumps({
            'item': '',
            'status': False
        })
        response = self.client.put('/buckets/1/items/1', data=item,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Missing parameters', response.data.decode())

    def test_edit_item_with_missing_bucket(self):
        """Should return 400 for missing bucket"""

        item = json.dumps({
            'item': 'Go to New York',
            'status': False
        })
        response = self.client.put('/buckets/1/items/1', data=item,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bucket with id 1 not found', response.data.decode())

    def test_edit_item_with_missing_item(self):
        """Should return 400 for missing item"""

        # First add the bucket
        bucket = json.dumps({
            'bucket': 'Travel',
            'desc': 'Visit places'
        })
        self.client.post('/buckets', data=bucket,
                         headers={"Authorization": self.token})
        item = json.dumps({
            'item': 'Go to New York',
            'status': False
        })
        response = self.client.put('/buckets/1/items/1', data=item,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('item with id 1 does not exist',
                      response.data.decode())

    def test_edit_item_with_invalid_status(self):
        """Should return 201 for item edited"""

        self.test_add_item_successfully()
        item = json.dumps({
            'item': 'Go to Silicon Valley',
            'status': "hello"
        })
        response = self.client.put('/buckets/1/items/1', data=item,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 409)
        self.assertIn('status should be true or false', response.data.decode())

    def test_edit_item_succesfully(self):
        """Should return 201 for item edited"""

        self.test_add_item_successfully()
        item = json.dumps({
            'item': 'Go to Silicon Valley',
            'status': False
        })
        response = self.client.put('/buckets/1/items/1', data=item,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Go to Silicon Valley', response.data.decode())

    def test_delete_item_that_doesnt_exist(self):
        """Should return 400 for missing item"""

        response = self.client.delete('/buckets/1/items/1',
                                      headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Item with id 1 does not exist', response.data.decode())

    def test_delete_item_successfully(self):
        """Should return 201 for item deleted"""

        self.test_add_item_successfully()
        response = self.client.delete('/buckets/1/items/1',
                                      headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Item deleted', response.data.decode())

    def tearDown(self):
        # Drop all tables
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
