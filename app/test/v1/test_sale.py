from unittest import TestCase
from app import create_app
import json


class TestSale(TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.sale = {'product_id': 1, 'name': 'sugar', 'cost': 10, 'amount': 1}

    def test_add_sale(self):
        path = '/api/v1/sales/'
        data = json.dumps(self.sale)
        # self.assertEqual(data, self.client.get('/api/v1/products/1').json['product'])
        result = self.client.post(
            path, data=data, content_type='application/json')
        self.assertEqual(201, result.status_code)
        self.assertEqual('success', result.json['message'])
        self.assertTrue(result.json['sale'])

    def test_get_all_sales(self):
        path = '/api/v1/sales'
        result = self.client.get(path)
        self.assertEqual(200, result.status_code)
        self.assertEqual('success', result.json['message'])
        self.assertTrue(result.json['sales'])

    def test_get_sales(self):
        path = '/api/v1/sales/1'
        result = self.client.get(path)
        self.assertEqual(200, result.status_code)
        self.assertEqual('success', result.json['message'])
        self.assertTrue(result.json['sale'])
