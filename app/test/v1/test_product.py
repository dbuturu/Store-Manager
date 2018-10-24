from unittest import TestCase
from app import create_app
import json

from .auth import *


class TestProduct(TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.add_user = add_user(self.client)
        self.admin_token = login_users(self.client)['admin_token']
        self.user_token = login_users(self.client)['user_token']
        self.product = {
            "name": "sugar",
            "cost": 10,
            "amount": 3
        }

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
        self.assertTrue(result.json['product'])
