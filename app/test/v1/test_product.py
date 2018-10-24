from unittest import TestCase
from app import create_app
import json


class TestProduct(TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.add_user()
        self.login_users()
        self.product = {
            "name": "sugar",
            "cost": 10,
            "amount": 3
        }

    def add_user(self):
        user_login = self.client.post(
            '/api/v1/users/',
            data=json.dumps(
                {
                    "username": "user",
                    "first_name": "store",
                    "last_name": "attendant",
                    "password": "password",
                    "email": "user@email.com",
                    "role": "store attendant"
                }
            ),
            content_type='application/json'
        )
        admin_login = self.client.post(
            '/api/v1/users/',
            data=json.dumps(
                {
                    "username": "admin",
                    "first_name": "store",
                    "last_name": "admin",
                    "password": "password",
                    "email": "admin@email.com",
                    "role": "admin"
                }
            ),
            content_type='application/json'
        )

    def login_users(self):
        user_login = self.client.post(
            '/api/v1/users/login/',
            data=json.dumps({
                "username": "admin",
                "password": "password"
            }),
            content_type='application/json'
        )
        self.user_token = user_login.data
        admin_login = self.client.post(
            "/api/v1/users/login",
            data=json.dumps({
                'username': 'admin',
                'password': 'password'
            }), content_type='application/json'
        )
        user_data = json.loads(user_login.data)
        admin_data = json.loads(admin_login.data)
        self.user_token = user_data["token"]
        self.admin_token = admin_data["token"]

    def test_add_product(self):
        path = '/api/v1/products/'
        product = json.dumps(self.product)
        result = self.client.post(
            path,
            headers={'Authorization': f"Bearer {self.admin_token}"},
            data=product,
            content_type='application/json'
        )
        self.assertEqual(201, result.status_code)
        self.assertEqual('success', result.json['message'])
        self.assertTrue(result.json['product'])

    def test_get_all_products(self):
        path = '/api/v1/products'
        result = self.client.get(path, headers=dict(
            Authorization="Bearer " + self.user_token))
        self.assertEqual(200, result.status_code)
        self.assertEqual('success', result.json['message'])
        self.assertTrue(result.json['products'])

    def test_get_products(self):
        path = '/api/v1/products/1'
        result = self.client.get(path, headers=dict(
            Authorization="Bearer " + self.admin_token))
        self.assertEqual(200, result.status_code)
        self.assertEqual('success', result.json['message'])
        self.assertTrue(result.json['product'])
