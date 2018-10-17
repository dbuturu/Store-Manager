from flask_restplus import Api
from flask import Blueprint
from werkzeug.exceptions import NotFound

v1 = Blueprint('v1', __name__, url_prefix="/api/v1")

from app.api.v1.views.product import end_point as products_end_points
#from app.api.v1.views.classname import ClassNames_end_points

api = Api(v1,
          title='Store Manger API',
          version='1.0',
          description="A simple Store mangment system")

api.add_namespace(products_end_points, path="/products/")
#api.add_namespace(ClassNames_end_points, path="/path")
