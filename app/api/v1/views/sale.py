from flask_restplus import Namespace, fields
from flask_restplus import Resource

from ..models.sale import Sale as SaleModel
from .product import product

sale = SaleModel()

end_point = Namespace('sales', description='sales resources')

sale_id = fields.Integer(required=True, description="The product id")

a_sale = end_point.model('sale', {
    'product_id': sale_id,
    'name': fields.String(required=True, description="The sales name"),
    'cost': fields.Integer(required=True, description="The sales cost"),
    'amount': fields.Integer(description="The amount of items to be sold")
})

message = end_point.model('message', {'message': fields.String(
    required=True, description="success or fail message")})

sale_message = end_point.model('sale message', {
    'message': fields.String(required=True, description="success or fail message"),
    'sale': fields.Nested(a_sale, skip_none=True)
})


@end_point.route('')
class Sale(Resource):
    @end_point.expect(a_sale)
    @end_point.doc('create a sale')
    @end_point.marshal_with(sale_message, code=201)
    def post(self):
        data = end_point.payload
        if data['product_id'] == 0 or data['name']=="":
            return {'message': 'Sorry could not add product'}, 404
        if not data['product_id'] and data['name'] and data['cost'] and data['amount']:
            return {'message': 'Sorry could not add product'}, 404
        sale.add(data['product_id'], data['name'],
                data['cost'], data['amount'])
        if not sale.get(sale.id):
            return {'message': 'Sorry could not add product'}, 404
        return {'message': 'success',
                'sale': sale.get(sale.id)
                }, 201

    @end_point.doc('read all sales')
    def get(self):
        if not sale.get_all():
            return {'message': 'Sorry no sales found',
                    'sales': {}
                    }, 404
        return {'message': 'success',
                'sales': sale.get_all()
                }, 200


@end_point.route('<sale_id>')
class SingleSale(Resource):
    @end_point.expect(sale_id)
    @end_point.doc('read all sales')
    @end_point.marshal_with(sale_message, code=200)
    def get(self, sale_id):
        if not sale.get(int(sale_id)):
            return {'message': 'Sorry this sale is not found'}, 404
        return {'message': 'success',
                'sale': sale.get(int(sale_id))
                }, 200

    @end_point.expect(sale_id, a_sale)
    @end_point.doc('update specific sale')
    @end_point.marshal_with(sale_message, code=200)
    def put(self, sale_id):
        data = end_point.payload
        if not sale.get(int(sale_id)):
            return {'message': 'Sorry this sale is not found'}, 404
        if sale.update(sale_id, {'name': data['name'], 'cost': data['cost'], 'amount': data['amount']}):
            return {
                'message': 'success',
                'sale': sale.get(int(sale_id))
            }, 200
        else:
            return{
                'message': 'Sorry could not update this sale order'
            }

    @end_point.expect(sale_id)
    @end_point.doc('delete specific sale')
    @end_point.marshal_with(message, code=200)
    def delete(self, sale_id):
        if not sale.get(int(sale_id)):
            return {'message': 'Sorry this sale is not found'}, 404
        if sale.delete(sale_id):
            return {'message': 'success'}, 200
        else:
            return{
                'message': 'Sorry could not delete this sale order'
            }
