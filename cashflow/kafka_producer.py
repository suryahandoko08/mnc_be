from kafka import KafkaProducer
import json

def send_transfer_to_queue(sender_id, recipient_id, amount, remarks):
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    transfer_data = {
        'sender_id': sender_id,
        'recipient_id': recipient_id,
        'amount': amount,
        'remarks': remarks
    }

    producer.send('transfer_topic', transfer_data)
    producer.flush()
