from unittest import TestCase
from app import create_app
import json


class TestProduct(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.product = {
            "name": "sugar",
            "cost": 10,
            "amount": 3
        }

    def test_add_product(self):
        path = '/api/v1/products/'
        data = json.dumps(self.product)
        result = self.client.post(path, data=data, content_type='application/json')
        self.assertEqual(201, result.status_code)
        self.assertEqual('success', result.json['message'])
        self.assertTrue(result.json['product'])

    def test_get_all_products(self):
        path = '/api/v1/products'
        result = self.client.get(path)
        self.assertEqual(200, result.status_code)
        self.assertEqual('success', result.json['message'])
        self.assertTrue(result.json['products'])

    def test_get_products(self):
        path = '/api/v1/products/1'
        result = self.client.get(path)
        self.assertEqual(200, result.status_code)
        self.assertEqual('success', result.json['message'])
        self.assertTrue(result.json['product'])
