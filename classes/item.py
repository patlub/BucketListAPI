from flask import jsonify
from modals.modals import BucketModal, ItemModal


class Item(object):
    """
    Handles all item operations
    """

    def add_item(self, user_id, bucket_id, item_name):
        """
        Creates a new bucket 
        """
        if not item_name:
            response = jsonify({'Error': 'Missing Item name'})
            response.status_code = 400
            return response

        bucket = BucketModal.query.filter_by(id=bucket_id,
                                             user_id=user_id).first()
        if not bucket:
            response = jsonify({'Error': 'Bucket with id '
                                         + str(user_id) + ' not found'})
            response.status_code = 400
            return response

        item = ItemModal(name=item_name, bucket_id=bucket_id)
        if item.query.filter_by(name=item_name).first():
            response = jsonify({'Error': 'item name Already exists'})
            response.status_code = 400
            return response

        item.save()
        response = jsonify({
            'Status': 'Successfully Added item',
            'id': item.id
        })
        response.status_code = 201
        return response