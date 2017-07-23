from datetime import datetime

from BucketListAPI import databases

class User(databases.Model):
    __table_name = 'users'
    id = databases.Column(databases.Integer, primary_key=True, autoincrement=True)
    name = databases.Column(databases.String(100))
    email = databases.Column(databases.String(100), unique=True)
    password = databases.Column(databases.String(200))
    bucket = databases.relationship('Bucket', backref='user')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def save(self):
        databases.session.add(self)
        databases.session.commit()

class Bucket(databases.Model):
    id = databases.Column(databases.Integer, primary_key=True, autoincrement=True)
    name = databases.Column(databases.String(50))
    desc = databases.Column(databases.String(100))
    date_added = databases.Column(databases.DateTime, default=datetime.utcnow())
    user_id = databases.Column(databases.Integer, databases.ForeignKey('user.id'))

    def __init__(self, name, desc):
        self.name = name
        self.desc = desc

    def save(self):
        databases.session.add(self)
        databases.session.commit()