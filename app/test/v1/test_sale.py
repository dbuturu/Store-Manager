from unittest import TestCase
from app import create_app
import json


class TestSale(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.add_user()
        self.login_users()
        self.sale = {'product_id': 1, 'name': 'sugar', 'cost': 10, 'amount': 1, "sold_by": "user"}

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
                "username": "user",
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

    def test_add_sale(self):
        path = '/api/v1/sales/'
        data = json.dumps(self.sale)
        # self.assertEqual(data, self.client.get('/api/v1/products/1').json['product'])
        result = self.client.post(
            path,
            headers={'Authorization': f"Bearer {self.user_token}"},
            data=data,
            content_type='application/json'
        )
        self.assertEqual(201, result.status_code)
        self.assertEqual('success', result.json['message'])
        self.assertTrue(result.json['sale'])

    def test_get_all_sales(self):
        path = '/api/v1/sales'
        result = self.client.get(path, headers={'Authorization': f"Bearer {self.user_token}"},)
        self.assertEqual(200, result.status_code)
        self.assertEqual('success', result.json['message'])
        self.assertTrue(result.json['sales'])

    def test_get_sales(self):
        path = '/api/v1/sales/1'
        result = self.client.get(path, headers={'Authorization': f"Bearer {self.admin_token}"},)
        self.assertEqual(200, result.status_code)
        self.assertEqual('success', result.json['message'])
        self.assertTrue(result.json['sale'])
