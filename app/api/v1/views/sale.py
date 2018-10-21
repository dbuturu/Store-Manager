from flask_restplus import Namespace, fields
from flask_restplus import Resource

from ..models.sale import Sale as SaleModel

sale = SaleModel()

end_point = Namespace('sales', description='sales resources')

sale_id = fields.Integer(required=True,description="The product id")

a_sale = end_point.model('sale', {
    'product_id': sale_id,
    'name': fields.String(required=True, description="The sales name"),
    'cost': fields.Integer(required=True, description="The sales cost"),
    'amount': fields.Integer(description="The amount of items to be sold")
})

sales = end_point.model('sales', {sale_id: fields.Nested(a_sale)})

message = end_point.model('message', {'message': fields.String(required=True, description="success or fail message")})

sale_message = end_point.model('sale message', {
    'message': fields.String(required=True, description="success or fail message"),
    'sale': fields.Nested(a_sale)
})


@end_point.route('')
class Sale(Resource):
    @end_point.expect(a_sale)
    @end_point.doc('create a sale')
    @end_point.marshal_with(sale_message, code=201)
    def post(self):
        data = end_point.payload
        sale.add(data['product_id'], data['name'], data['cost'], data['amount'])
        return {'message': 'success',
                'sale': sale.get(sale.id)
                }, 201
