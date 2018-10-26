from flask import Flask
from flask_jwt_extended import JWTManager
from werkzeug.contrib.fixers import ProxyFix

from app.api.v1 import v1
from app.api.v1.views.user import blacklist
from instance.config import app_config
from app.api.v1.models.user import User

users = User()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.url_map.strict_slashes = False
    app.config['SWAGGER_UI_JSONEDITOR'] = True
    app.config['SECRET_KEY'] = 'hidenkey'

    app.wsgi_app = ProxyFix(app.wsgi_app)

    jwt = JWTManager(app)

    @jwt.user_claims_loader
    def add_user_claims_loader(username):
        return {"roles":users.get(username).get('role')}

    @jwt.user_identity_loader
    def user_identity_loader(user):
        return user

    @jwt.token_in_blacklist_loader
    def token_in_blacklist_loader(decrypted_token):
        json_token_identifier = decrypted_token['jti']
        return json_token_identifier in blacklist

    app.register_blueprint(v1)
    return app
