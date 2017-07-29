from datetime import datetime

from api.__init__ import db


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

    def __init__(self, email, password, name=None):
        self.email = email
        self.password = password
        self.name = name

    def save(self):
        """
        Save User to DB        
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Get all Users"""
        return User.query.all()

    def delete(self):
        """Delete User"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<User: {}>".format(self.name)


class Bucket(db.Model):
    """
    Bucket database Modal
    """
    __table_name = 'buckets'
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

    @staticmethod
    def get_all():
        """Get all Buckets"""
        Bucket.query.all()

    def delete(self):
        """Delete Bucket"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<Bucket: {}>".format(self.name)


class Item(db.Model):
    """
    Item Database Modal
    """
    __table_name = 'items'
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

    @staticmethod
    def get_all():
        """Get all Items"""
        Item.query.all()

    def delete(self):
        """Delete Item"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<Item: {}>".format(self.name)
