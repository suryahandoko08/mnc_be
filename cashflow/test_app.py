import unittest
from app import app, db
from models import User
from flask import jsonify
import json

class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

   
    # Test for /register API
    def test_register(self):
        response = self.app.post('/register', json={
            'first_name': 'Guntur',
            'last_name': 'Saputro',
            'phone_number': '0811255501',
            'address': 'Jl. Kebon Sirih No. 1',
            'pin': '123456'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'SUCCESS')

    # Test for /login API
    def test_login(self):
        # Register user first
        self.app.post('/register', json={
            'first_name': 'Guntur',
            'last_name': 'Saputro',
            'phone_number': '0811255501',
            'address': 'Jl. Kebon Sirih No. 1',
            'pin': '123456'
        })
        # Login with the registered user
        response = self.app.post('/login', json={
            'phone_number': '0811255501',
            'pin': '123456'
        })
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data['result'])

    # Test for /topup API
    def test_topup(self):
        # Register user
        self.app.post('/register', json={
            'first_name': 'Guntur',
            'last_name': 'Saputro',
            'phone_number': '0811255501',
            'address': 'Jl. Kebon Sirih No. 1',
            'pin': '123456'
        })
        # Top up balance
        response = self.app.post('/topup', json={
            'amount': 500000
        }, headers={'Authorization': 'Bearer <JWT_TOKEN>'})
        self.assertEqual(response.status_code, 201)

    # Test for /pay API
    def test_payment(self):
        # Register user
        self.app.post('/register', json={
            'first_name': 'Guntur',
            'last_name': 'Saputro',
            'phone_number': '0811255501',
            'address': 'Jl. Kebon Sirih No. 1',
            'pin': '123456'
        })
        # Payment
        response = self.app.post('/pay', json={
            'amount': 100000,
            'remarks': 'Pulsa Telkomsel 100k'
        }, headers={'Authorization': 'Bearer <JWT_TOKEN>'})
        self.assertEqual(response.status_code, 201)

    # Test for /transfer API
    def test_transfer(self):
        # Register users
        self.app.post('/register', json={
            'first_name': 'Guntur',
            'last_name': 'Saputro',
            'phone_number': '0811255501',
            'address': 'Jl. Kebon Sirih No. 1',
            'pin': '123456'
        })
        self.app.post('/register', json={
            'first_name': 'Dewi',
            'last_name': 'Anita',
            'phone_number': '0811255502',
            'address': 'Jl. Kebon Sirih No. 2',
            'pin': '654321'
        })
        # Transfer balance
        response = self.app.post('/transfer', json={
            'target_user': '0811255502',
            'amount': 30000,
            'remarks': 'Hadiah Ultah'
        }, headers={'Authorization': 'Bearer <JWT_TOKEN>'})
        self.assertEqual(response.status_code, 201)

    # Test for /transactions API
    def test_transactions_report(self):
        # Register user
        self.app.post('/register', json={
            'first_name': 'Guntur',
            'last_name': 'Saputro',
            'phone_number': '0811255501',
            'address': 'Jl. Kebon Sirih No. 1',
            'pin': '123456'
        })
        # Get transactions
        response = self.app.get('/transactions', headers={'Authorization': 'Bearer <JWT_TOKEN>'})
        self.assertEqual(response.status_code, 200)

    # Test for /profile API
    def test_update_profile(self):
        # Register user
        self.app.post('/register', json={
            'first_name': 'Guntur',
            'last_name': 'Saputro',
            'phone_number': '0811255501',
            'address': 'Jl. Kebon Sirih No. 1',
            'pin': '123456'
        })
        # Update profile
        response = self.app.put('/profile', json={
            'first_name': 'Tom',
            'last_name': 'Araya',
            'address': 'Jl. Diponegoro No. 215'
        }, headers={'Authorization': 'Bearer <JWT_TOKEN>'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
