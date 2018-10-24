from ..models.product import Product as ProductModel
from flask_restplus import Resource, Namespace, fields
from  flask_jwt_extended import jwt_required

from ..views import requires_permission

product = ProductModel()

end_point = Namespace('products', description='products resources')

product_id = fields.Integer(description="The products id")

a_product = end_point.model('product', {
    'name': fields.String(required=True, description="The products name", skip_none=True),
    'cost': fields.Integer(required=True, description="The products cost", skip_none=True),
    'amount': fields.Integer(required=True, description="The amount of the product", skip_none=True)
}, skip_none=True)

message = end_point.model('message', {'message': fields.String(
    required=True, description="success or fail message")})

product_message = end_point.model('product message', {
    'message': fields.String(required=True, description="success or fail message"),
    'product': fields.Nested(a_product, skip_none=True)
})


@end_point.route('')
class Product(Resource):
    @requires_permission('admin')
    @end_point.expect(a_product)
    @end_point.doc('Add a product')
    @end_point.marshal_with(product_message, code=201)
    def post(self):
        data = end_point.payload
        if not data['name'] and data['cost'] and data['amount']:
            return {'message': 'Sorry could not add product'}, 404
        product.add(data['name'], data['cost'], data['amount'])
        return {'message': 'success',
                'product': product.get(product.id)
                }, 201

    @jwt_required
    @end_point.doc('read all products')
    def get(self):
        if not product.get_all():
            return {'message': 'Sorry no products found',
                    'product': {}
                    }, 404
        return {'message': 'success',
                'products': product.get_all()
                }, 200


@end_point.route('<product_id>')
class SingleProduct(Resource):
    @requires_permission('store attendant')
    @end_point.expect(product_id)
    @end_point.doc('read specific product')
    @end_point.marshal_with(product_message, code=200)
    def get(self, product_id):
        item = product.get(int(product_id))
        if not item:
            return {'message': 'Sorry this product is not found'}, 404
        return {
            'product': item
        }, 200

    @requires_permission('admin')
    @end_point.expect(product_id, a_product)
    @end_point.doc('update specific product')
    @end_point.marshal_with(product_message, code=200)
    def put(self, product_id):
        req = end_point.payload
        if not product.get(int(product_id)):
            return {'message': 'Sorry this product is not found'}, 404
        data = {'name': req['name'],
                'cost': req['cost'], 'amount': req['amount']}
        if product.update(product_id, data):
            return {
                'message': 'Product has been Successfully Updated',
                'product': product.get(int(product_id))
            }, 200
        else:
            return{
                'message': 'Sorry could not update this product'
            }

    @requires_permission('admin')
    @end_point.expect(product_id)
    @end_point.doc('delete specific product')
    @end_point.marshal_with(message, code=200)
    def delete(self, product_id):
        if not product.get(int(product_id)):
            return {'message': 'Sorry this product is not found'}, 404
        if product.delete(product_id):
            return {'message': 'Product has been Successfully Deleted'}, 200
        else:
            return{
                'message': 'Sorry could not delete this product'
            }
