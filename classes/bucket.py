from flask import jsonify
from modals.modals import BucketModal, ItemModal


class Bucket(object):
    """
    Handles all bucket operations
    """

    @staticmethod
    def create_bucket(name, desc, user_id):
        """
        Creates a new bucket
        :param name: 
        :param desc: 
        :param user_id: 
        :return: 
        """
        if not name:
            response = jsonify({'Error': 'Missing name'})
            response.status_code = 200
            return response

        bucket = BucketModal(name=name, desc=desc, user_id=user_id)
        if bucket.query.filter_by(name=name).first():
            response = jsonify({'Error': 'Bucket name Already exists'})
            response.status_code = 409
            return response

        bucket.save()
        response = jsonify({
            'id': bucket.id,
            'name': bucket.name,
            'desc': bucket.desc,
            'date_added': bucket.date_added,
            'user_id': bucket.user_id
        })
        response.status_code = 201
        return response

    @staticmethod
    def get_buckets(user_id, search, limit=None):
        """
        Gets all buckets
        :param user_id: 
        :param search: 
        :return: 
        """

        response = BucketModal.query.limit(limit).all()
        if not response:
            response = jsonify({'error': 'No bucketlist has been created'})
            response.status_code = 200
            return response
        else:
            if search:
                res = [bucket for bucket in response if bucket.name
                       in search and bucket.user_id == user_id]
                if not res:
                    response = jsonify({
                        'error': 'The bucket you searched does not exist'
                    })
                    return response
                else:
                    bucketlist_data = []
                    for data in res:
                        final = {
                            'id': data.id,
                            'name': data.name,
                            'desc': data.desc,
                            'date_added': data.date_added,
                            'user_id': data.user_id
                        }
                        bucketlist_data.clear()
                        bucketlist_data.append(final)
                    response = jsonify(bucketlist_data)
                    response.status_code = 200
                    return response

            else:
                res = [bucket for bucket in
                       response if bucket.user_id == user_id]
                bucketlist_data = []
                if not res:
                    response = jsonify({
                        'error': 'No bucketlists have been created'
                    })
                    response.status_code = 200
                    return response
                else:
                    for data in res:
                        final = {
                            'id': data.id,
                            'name': data.name,
                            'desc': data.desc,
                            'date_added': data.date_added,
                            'user_id': data.user_id
                        }
                        bucketlist_data.append(final)
                    response = jsonify(bucketlist_data)
                    response.status_code = 200
                    return response

    @staticmethod
    def get_single_bucket(user_id, bucket_id):
        """
        Gets single bucket
        :param user_id: 
        :param bucket_id: 
        """
        bucket = BucketModal.query.filter_by(id=bucket_id,
                                             user_id=user_id).first()
        if not bucket:
            response = jsonify({
                'error': 'bucketlist with id ' +
                         str(bucket_id) + ' not found'
            })
            response.status_code = 200
            return response

        bucket_data = {
            'id': bucket.id,
            'name': bucket.name,
            'desc': bucket.desc,
            'date_added': bucket.date_added,
            'user_id': bucket.user_id
        }
        response = jsonify(bucket_data)
        response.status_code = 200
        return response

    @staticmethod
    def update_bucket(user_id, bucket_id, bucket_name, desc):
        """
        Updates a bucket
                
        :param user_id: 
        :param bucket_id: 
        :param bucket_name: 
        :param desc:  
        """
        if not bucket_name:
            response = jsonify({'Error': 'Missing Bucket name'})
            response.status_code = 200
            return response

        bucket = BucketModal.query.filter_by(id=bucket_id,
                                             user_id=user_id).first()
        if not bucket:
            bucket = jsonify({'error': 'the bucket does not exist'})
            bucket.status_code = 200
            return bucket

        if bucket.query.filter_by(name=bucket_name).first():
            response = jsonify({'Error': 'Bucket name Already exists'})
            response.status_code = 409
            return response


        bucket.name = bucket_name
        bucket.desc = desc
        bucket.update()

        bucket = BucketModal.query.filter_by(id=bucket_id,
                                             user_id=user_id).first()
        response = jsonify({
            'success': 'bucket updated',
            'bucket': bucket.name
        })
        response.status_code = 200
        return response

    @staticmethod
    def delete_bucket(user_id, bucket_id):
        """
        Deletes a bucket        
        :param user_id: 
        :param bucket_id: 
        """
        bucket = BucketModal.query.filter_by(id=bucket_id,
                                             user_id=user_id).first()
        if not bucket:
            response = jsonify({'error': 'Bucket not found'})
            response.status_code = 200
            return response

        items = ItemModal.query.filter_by(bucket_id=bucket_id)
        if items:
            for item in items:
                item.delete()

        bucket.delete()
        response = jsonify({
            'success': 'bucket deleted'
        })
        response.status_code = 200
        return response
