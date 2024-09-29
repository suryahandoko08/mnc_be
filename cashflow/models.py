from extensions import db
import uuid
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String, nullable=False)
    pin = db.Column(db.String, nullable=False)
    balance = db.Column(db.Integer, default=0)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'user_id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone_number': self.phone_number,
            'address': self.address,
            'balance': self.balance,
            'created_date': self.created_date
        }

class Transaction(db.Model):
    __tablename__ = 'transaction'
    
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.String, nullable=True)
    transaction_type = db.Column(db.String, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'user_id': self.id,
            'amount': self.amount,
            'remarks': self.remarks,
            'transaction_type': self.transaction_type,
            'created_date': self.created_date,
        }
