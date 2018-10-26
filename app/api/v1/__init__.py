from flask_restplus import Api
from flask import Blueprint

from app.api.v1.views.product import end_point as products_end_points
from app.api.v1.views.sale import end_point as sales_end_points
from app.api.v1.views.user import end_point as users_end_points
# from app.api.v1.views.class_name import ClassNames_end_points

v1 = Blueprint('v1', __name__, url_prefix="/api/v1")

api = Api(
    v1,
    title='Store Manger API',
    version='1.0',
    description="A simple Store mangment system"
)

api.add_namespace(products_end_points, path="/products/")
api.add_namespace(sales_end_points, path="/sales/")
api.add_namespace(users_end_points, path="/users/")
# api.add_namespace(ClassNames_end_points, path="/path")
