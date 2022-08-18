from datetime import datetime
from email.policy import default
from enum import unique
from turtle import back
from werkzeug.security import generate_password_hash
from app import db, login
from flask_login import UserMixin

class Address(db.Model):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.String(15), nullable = False)
    address = db.Column(db.String(255), nullable = False, unique = True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), nullable = False, unique = True)
    username = db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    addressbook = db.relationship('Address', backref='user', lazy='dynamic')
    
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


