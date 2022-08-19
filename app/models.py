from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from flask_login import UserMixin

class Address(db.Model):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.String(15), nullable = False, unique = True )
    street = db.Column(db.String(255), nullable = False)
    city = db.Column(db.String(50), nullable = False)
    state = db.Column(db.String(20), nullable = False)
    zipcode = db.Column(db.String(10) ,nullable = False)
    county = db.Column(db.String(40), nullable = False)
    address_type = db.Column(db.String(30), nullable = False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'name','phone','street','city','state','zipcode','county','address_type','user_id'}:
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class User(db.Model, UserMixin):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.set_password(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), nullable = False, unique = True)
    username = db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.String(255), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    addressbook = db.relationship('Address', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


