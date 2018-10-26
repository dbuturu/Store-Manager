from unittest import TestCase
from app import create_app
import json

from .auth import *

class TestSale(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.add_user = add_user(self.client)
        self.admin_token = login_users(self.client)['admin_token']
        self.user_token = login_users(self.client)['user_token']
        self.sale = {'product_id': 1, 'name': 'sugar', 'cost': 10, 'amount': 1, "sold_by": "user"}

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
        self.assertEqual('Sale order has been Successfully created', result.json['message'])
        self.assertTrue(result.json['sale'])

    def test_get_all_sales(self):
        path = '/api/v1/sales'
        result = self.client.get(path, headers={'Authorization': f"Bearer {self.user_token}"},)
        self.assertEqual(200, result.status_code)
        self.assertEqual('Sale orders has been Successfully found', result.json['message'])
        self.assertTrue(result.json['sales'])

    def test_get_sales(self):
        path = '/api/v1/sales/1'
        result = self.client.get(path, headers={'Authorization': f"Bearer {self.admin_token}"},)
        self.assertEqual(200, result.status_code)
        self.assertEqual('Sale order has been Successfully found', result.json['message'])
        self.assertTrue(result.json['sale'])
