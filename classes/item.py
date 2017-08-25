from flask import jsonify
from modals.modals import BucketModal, ItemModal


class Item(object):
    """
    Handles all item operations
    """

    @staticmethod
    def get_items(bucket_id):
        """
        Gets all items
        :param bucket_id: 
        :return: 
        """
        response = ItemModal.query.all()
        if not response:
            response = jsonify({'error': 'No item has been created'})
            response.status_code = 200
            return response
        else:
            res = [item for item in
                   response if item.bucket_id == bucket_id]
            item_data = []
            for data in res:
                final = {
                    'id': data.id,
                    'name': data.name,
                    'status': data.status,
                    'date_added': data.date_added,
                    'bucket_id' : data.bucket_id
                }
                item_data.append(final)
            response = jsonify(item_data)
            response.status_code = 200
            return response

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
            response.status_code = 200
            return response

        bucket = BucketModal.query.filter_by(id=bucket_id,
                                             user_id=user_id).first()
        if not bucket:
            response = jsonify({'Error': 'Bucket with id '
                                         + str(user_id) + ' not found'})
            response.status_code = 200
            return response

        item = ItemModal(name=item_name, bucket_id=bucket_id)
        if item.query.filter_by(name=item_name).first():
            response = jsonify({'Error': 'item name Already exists'})
            response.status_code = 200
            return response

        item.save()
        response = jsonify({
            'id': item.id,
            'name': item.name,
            'status': item.status,
            'date_added': item.date_added
        })
        response.status_code = 201
        return response

    @staticmethod
    def edit_item(user_id, bucket_id, item_id, new_item_name, new_item_status):
        """
        Edits an item

        :param user_id: 
        :param bucket_id: 
        :param item_id: 
        :param new_item_name: 
        :param new_item_status: 
        """
        if not new_item_name and not new_item_status:
            response = jsonify({'Error': 'Missing parameters'})
            response.status_code = 200
            return response

        allowed_status = ["true", "false"]
        if new_item_status not in allowed_status:
            response = jsonify({'Error': 'status should be true or false'})
            response.status_code = 409
            return response

        bucket = BucketModal.query.filter_by(id=bucket_id,
                                             user_id=user_id).first()
        if not bucket:
            response = jsonify({'Error': 'Bucket with id '
                                         + str(user_id) + ' not found'})
            response.status_code = 200
            return response

        item = ItemModal.query.filter_by(id=item_id, bucket_id=bucket_id).first()
        if not item:
            response = jsonify({
                'Error': 'item with id ' + str(item_id) + ' does not exist'
            })
            response.status_code = 200
            return response

        item.name = new_item_name
        item.status = new_item_status
        item.save()
        response = jsonify({
            'item_name': new_item_name,
            'status': item.status
        })
        response.status_code = 201
        return response

    @staticmethod
    def delete_item(item_id):
        """
        Deletes an item

        :param item_id:  
        """
        item = ItemModal.query.filter_by(id=item_id).first()
        if not item:
            response = jsonify({
                'Error': 'Item with id '
                         + str(item_id) + ' does not exist '
            })
            response.status_code = 200
            return response

        item.delete()
        response = jsonify({
            'success': 'Item deleted'
        })
        response.status_code = 201
        return response
