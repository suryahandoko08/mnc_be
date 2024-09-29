from kafka import KafkaConsumer
from models import User, Transaction
from extensions import db
from app import app  
import json
import uuid
import datetime

def process_transfer():
    consumer = KafkaConsumer(
        'transfer_topic',
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='transfer_consumer_group'
    )

    with app.app_context(): 
        for message in consumer:
            transfer_data = message.value
            sender_id = transfer_data['sender_id']
            recipient_id = transfer_data['recipient_id']
            amount = transfer_data['amount']
            remarks = transfer_data['remarks']

            sender = User.query.get(sender_id)
            recipient = User.query.get(recipient_id)

            if sender and recipient and sender.balance >= amount:
                sender.balance -= amount
                recipient.balance += amount
                transfer_id = str(uuid.uuid4())
                transaction = Transaction(
                    id=transfer_id,
                    user_id=sender_id,
                    amount=amount,
                    remarks=remarks,
                     transaction_type='DEBIT',
                     created_date=datetime.datetime.utcnow()
                )
                db.session.add(transaction)
                db.session.commit()

                print(f"Transfer {amount} success from {sender_id} to {recipient_id}")
            else:
                print(f"Fail transfer, balance {sender_id} not enough or invalid users")

if __name__ == '__main__':
    process_transfer()
