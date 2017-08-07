from flask import jsonify
from modals.modals import BucketModal, ItemModal


class Item(object):
    """
    Handles all item operations
    """

    @staticmethod
    def add_item(user_id, bucket_id, item_name):
        """
        Adds an item
                
        :param user_id: 
        :param bucket_id: 
        :param item_name: 
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

    @staticmethod
    def edit_item(user_id, bucket_id, item_id, new_item_name):
        """
        Edits an item

        :param user_id: 
        :param bucket_id: 
        :param item_id: 
        :param new_item_name: 
        """
        if not new_item_name:
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

        item = ItemModal.query.filter_by(id=item_id, bucket_id=bucket_id).first()
        if not item:
            response = jsonify({
                'Error': 'item with id ' + str(item_id) + ' does not exist'
            })
            response.status_code = 400
            return response

        item.name = new_item_name
        item.save()
        response = jsonify({
            'Status': 'Successfully updated item',
            'item_name': new_item_name
        })
        response.status_code = 201
        return response

    @staticmethod
    def delete_item(user_id, item_id):
        """
        Deletes an item

        :param user_id: 
        :param bucket_id:  
        """
        item = ItemModal.query.filter_by(id=item_id).first()
        if not item:
            response = jsonify({
                'Error': 'Item with id '
                         + str(item_id) + ' does not exist '
            })
            response.status_code = 400
            return response

        item.delete()
        response = jsonify({
            'success': 'Item deleted'
        })
        response.status_code = 201
        return response