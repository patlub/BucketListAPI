from flask import jsonify
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

    def get_buckets(self, user_id, search):
        response = BucketModal.query.all()
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

    def get_single_bucket(self, user_id, bucket_id):
        bucket = BucketModal.query.filter_by(id=bucket_id,
                                             user_id=user_id).first()
        if not bucket:
            response = jsonify({
                'error': 'bucketlist with id ' +
                         str(bucket_id) + ' not found'
            })
            response.status_code = 400
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

    def update_bucket(self, user_id, bucket_id, bucket_name, desc):
        if not bucket_name:
            response = jsonify({'Error': 'Missing Bucket name'})
            response.status_code = 400
            return response

        bucket = BucketModal.query.filter_by(id=bucket_id,
                                             user_id=user_id).first()
        if not bucket:
            bucket = jsonify({'error': 'the bucket does not exist'})
            bucket.status_code = 400
            return bucket

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

    def delete_bucket(self, user_id, bucket_id):
        bucket = BucketModal.query.filter_by(id=bucket_id,
                                             user_id=user_id).first()
        if not bucket:
            bucket = jsonify({'error': 'Bucket not found'})
            bucket.status_code = 400
            return bucket

        bucket.delete()
        response = jsonify({
            'success': 'bucket deleted',
        })
        response.status_code = 200
        return response
