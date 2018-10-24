from flask import Flask, jsonify
from instance.config import app_config
from werkzeug.contrib.fixers import ProxyFix
from flask_jwt_extended import JWTManager, get_jwt_claims, verify_jwt_in_request, get_jwt_identity
from functools import wraps

from app.api.v1 import v1
from app.api.v1.views.user import blacklist


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['roles'] != 'admin':
            return jsonify(msg='Admins only'), 403
        else:
            return fn(*args, **kwargs)
    return wrapper

def owner_required(owner):
    def decorator(fn):
        def decorated(*args,**kwargs):
            identity = get_jwt_identity()
            if owner is identity:
                return fn(*args,**kwargs)
            return jsonify(msg='Admins and Owner only'), 403
        return decorated
    return decorator

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.url_map.strict_slashes = False
    app.config['SWAGGER_UI_JSONEDITOR'] = True

    app.wsgi_app = ProxyFix(app.wsgi_app)

    jwt = JWTManager(app)

    @jwt.user_claims_loader
    def add_user_claims_loader(user):
        return {'role': user['role']}

    @jwt.user_identity_loader
    def user_identity_loader(user):
        return user["username"]

    @jwt.token_in_blacklist_loader
    def token_in_blacklist_loader(decrypted_token):
        json_token_identifier = decrypted_token['jti']
        return json_token_identifier in blacklist

    @jwt.user_loader_error_loader
    def custom_user_loader_error(identity):
        return {'message': "User {} not found".format(identity)}, 404

    app.register_blueprint(v1)
    return app
