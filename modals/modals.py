from datetime import datetime

from api import db
from werkzeug.security import generate_password_hash, \
    check_password_hash


class UserModal(db.Model):
    """
    User Database Modal
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))

    def __init__(self, email, password, name=None):
        self.email = email
        self.name = name
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def save(self):
        """
        Save User to DB        
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Get all Users"""
        return UserModal.query.all()

    def delete(self):
        """Delete User"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<User: {}>".format(self.name)


class BucketModal(db.Model):
    """
    Bucket database Modal
    """
    __tablename__ = 'buckets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

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
        BucketModal.query.all()

    def delete(self):
        """Delete Bucket"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<Bucket: {}>".format(self.name)


class ItemModal(db.Model):
    """
    Item Database Modal
    """
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(5))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    bucket_id = db.Column(db.Integer, db.ForeignKey('buckets.id'))

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
        ItemModal.query.all()

    def delete(self):
        """Delete Item"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<Item: {}>".format(self.name)
