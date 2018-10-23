from flask import Flask
from instance.config import app_config
from werkzeug.contrib.fixers import ProxyFix
from flask_jwt_extended import JWTManager


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.url_map.strict_slashes = False
    app.config['SWAGGER_UI_JSONEDITOR'] = True

    app.wsgi_app = ProxyFix(app.wsgi_app)

    jwt.init_app(app)

    from app.api.v1 import v1
    app.register_blueprint(v1)
    jwt = JWTManager(app)
    return app
