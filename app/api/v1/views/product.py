from ..models.product import Product as ProductModel
from flask_restplus import Resource
from flask import request, jsonify
import json
from flask_restplus import Namespace, fields

product = ProductModel()

end_point = Namespace('products', description='products resources')

product_id = fields.Integer(description="The products id")

a_product = end_point.model('product', {
    'name': fields.String(required=True, description="The products name"),
    'cost': fields.Integer(required=True, description="The products cost"),
    'amount': fields.Integer(required=True, description="The amount of the product")
})

products = end_point.model('products', {product_id: fields.Nested(a_product)})

message = end_point.model('message', {'message': fields.String(required=True, description="success or fail message")})

product_message = end_point.model('product message', {
    'message': fields.String(required=True, description="success or fail message"),
    'product': fields.Nested(a_product)
})


@end_point.route('')
class Product(Resource):
    @end_point.expect(a_product)
    @end_point.doc('create a product')
    @end_point.marshal_with(product_message, code=201)
    def post(self):
        data = end_point.payload
        product.add(data['name'], data['cost'], data['amount'])
        return {'message': 'success',
                'product': product.get(product.id)
                }, 201

    @end_point.doc('read all products')
    # @end_point.marshal_with(products, code=200)
    def get(self):
        if not product.get_all():
            return {'message': 'Sorry no products found',
                    'product': {}
                    }, 404
        return {'message': 'success',
                'products': product.get_all()
                }, 200
