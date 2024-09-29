from flask import request, jsonify
from app import app, db
from kafka_producer import send_transfer_to_queue
from models import User, Transaction
import jwt
import datetime
from functools import wraps
import uuid

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        if not token:
            return jsonify({'message': 'Unauthenticated'}), 401
        try:
            data = jwt.decode(token, 'secret_key', algorithms=["HS256"])
            current_user = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        return f(current_user, *args, **kwargs)
    return decorator

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    existing_user = User.query.filter_by(phone_number=data['phone_number']).first()
    if existing_user:
        return jsonify({'message': 'Phone Number already registered'}), 400
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone_number=data['phone_number'],
        address=data['address'],
        pin=data['pin']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'status': 'SUCCESS', 'result': new_user.to_dict()}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(phone_number=data['phone_number'], pin=data['pin']).first()
    if user:
        token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)}, 'secret_key', algorithm="HS256")
        return jsonify({'status': 'SUCCESS', 'result': {'access_token': token}}), 200
    return jsonify({'message': 'Phone Number and PIN doesn’t match.'}), 401

@app.route('/topup', methods=['POST'])
@token_required
def topup(current_user):
    data = request.json
    amount = data['amount']
    user = User.query.get(current_user)
    user.balance += amount
    top_up_id = str(uuid.uuid4())
    transaction = Transaction(
        id=top_up_id,
        user_id=current_user,
        amount=amount,
        transaction_type='CREDIT',
        created_date=datetime.datetime.utcnow()
    )
    db.session.add(transaction)
    db.session.commit()

    return jsonify({
        'status': 'SUCCESS',
        'result': {
            'top_up_id': top_up_id,
            'amount_top_up': amount,
            'balance_before': user.balance - amount,
            'balance_after': user.balance,
            'created_date': transaction.created_date
        }
    }), 200

@app.route('/pay', methods=['POST'])
@token_required
def pay(current_user):
    data = request.json
    amount = data['amount']
    remarks = data['remarks']
    user = User.query.get(current_user)

    if user.balance >= amount:
        user.balance -= amount
        payment_id = str(uuid.uuid4())
        transaction = Transaction(
            id=payment_id,
            user_id=current_user,
            amount=amount,
            remarks=remarks,
            transaction_type='DEBIT',
            created_date=datetime.datetime.utcnow()
        )
        db.session.add(transaction)
        db.session.commit()

        return jsonify({
            'status': 'SUCCESS',
            'result': {
                'payment_id': payment_id,
                'amount': amount,
                'remarks': remarks,
                'balance_before': user.balance + amount,
                'balance_after': user.balance,
                'created_date': transaction.created_date
            }
        }), 200
    else:
        return jsonify({'message': 'Balance is not enough'}), 400


#if using Background Process using Kafka 
@app.route('/transfer_queue', methods=['POST'])
@token_required
def transfer_queue(current_user):
    data = request.json
    user = User.query.get(current_user)
    recipient_id = data['target_user']
    amount = data['amount']
    remarks = data['remarks']
    send_transfer_to_queue(user.id, recipient_id, amount, remarks)

    return jsonify({'status': 'SUCCESS', 'message': 'Transfer in process'}), 202

@app.route('/transfer', methods=['POST'])
@token_required
def transfer(current_user):
    data = request.json
    target_user_id = data['target_user']
    amount = data['amount']
    remarks = data['remarks']
    
    user = User.query.get(current_user)
    target_user = User.query.get(target_user_id)
    if user.balance >= amount and target_user:
        user.balance -= amount
        target_user.balance += amount

        transfer_id = str(uuid.uuid4())
        transaction = Transaction(
            id=transfer_id,
            user_id=current_user,
            amount=amount,
            remarks=remarks,
            transaction_type='DEBIT',
            created_date=datetime.datetime.utcnow()
        )
        db.session.add(transaction)
        db.session.commit()

        return jsonify({
            'status': 'SUCCESS',
            'result': {
                'transfer_id': transfer_id,
                'amount': amount,
                'remarks': remarks,
                'balance_before': user.balance + amount,
                'balance_after': user.balance,
                'created_date': transaction.created_date
            }
        }), 200
    else:
        return jsonify({'message': 'Balance is not enough or target user not found.'}), 400

@app.route('/transactions', methods=['GET'])
@token_required
def transactions(current_user):
    transactions = Transaction.query.filter_by(user_id=current_user).all()
    return jsonify({
        'status': 'SUCCESS',
        'result': [transaction.to_dict() for transaction in transactions]
    }), 200

@app.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    data = request.json
    user = User.query.get(current_user)

    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'address' in data:
        user.address = data['address']

    db.session.commit()

    return jsonify({
        'status': 'SUCCESS',
        'result': {
            'user_id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'address': user.address,
            'updated_date': datetime.datetime.utcnow()
        }
    }), 200
