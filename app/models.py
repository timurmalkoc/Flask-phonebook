from datetime import datetime
from enum import unique
from app import db

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
