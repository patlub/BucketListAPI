from flask import jsonify
from validate_email import validate_email
from modals.modals import BucketModal


class Bucket(object):
    """
    Handles all bucket operations
    """
    def create_bucket(self, name, desc, user_id):
        """
        Creates a new bucket 
        """
        if not name:
            response = jsonify({'Error': 'Missing name'})
            response.status_code = 400
            return response

        bucket = BucketModal(name=name, desc=desc, user_id=user_id)
        if bucket.query.filter_by(name=name).first():
            response = jsonify({'Error': 'Bucket name Already exists'})
            response.status_code = 400
            return response

        bucket.save()
        response = jsonify({
            'Status': 'Successfully Added bucket',
            'id': bucket.id
        })
        response.status_code = 201
        return response