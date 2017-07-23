from datetime import datetime

from BucketListAPI import db


class User(db.Model):
    """
    User Database Modal
    """
    __table_name = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    bucket = db.relationship('Bucket', backref='user')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def save(self):
        """
        Save User to DB        
        """
        db.session.add(self)
        db.session.commit()


class Bucket(db.Model):
    """
    Bucket database Modal
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    item = db.relationship('Item', backref='bucket')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def save(self):
        """
        Save Bucket to DB
        """
        db.session.add(self)
        db.session.commit()


class Item(db.Model):
    """
    Item Database Modal
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(5))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    bucket_id = db.Column(db.Integer, db.ForeignKey('bucket.id'))

    def __init__(self, name, status):
        self.name = name
        self.status = status

    def save(self):
        """
        Save Item to DB
        """
        db.session.add(self)
        db.session.commit()
