from ..models.user import User as UserModel
from flask_restplus import Resource, Namespace, fields
from flask import request, jsonify
import json
from flask_jwt_extended import (
    JWTManager,create_access_token,
    create_refresh_token, get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    jwt_refresh_token_required
)

jwt = JWTManager()

authapi = Namespace('auth', description='Authorization API')

creds = authapi.model('Credentials', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
})

user = UserModel()


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    if not User.objects(username__exact=identity):
        return None

    return User.objects(username__exact=identity).get()


@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    ret = {
        "msg": "User {} not found".format(identity)
    }
    return jsonify(ret), 404


end_point = Namespace('users', description='users resources')

username = fields.String(description="The users username")

a_user = end_point.model('user', {
    'username': username,
    'first_name': fields.String(required=True, description="The user's first name"),
    'last_name': fields.String(required=True, description="The user's last name"),
    'email': fields.String(required=True, description="The user's email")
})

new_user = end_point.model('user', {
    'username': username,
    'first_name': fields.String(required=True, description="The user's first name"),
    'last_name': fields.String(required=True, description="The user's last name"),
    'password': fields.String(required=True, description="The user's password"),
    'email': fields.String(required=True, description="The user's email")
})

users = end_point.model('users', {'username': fields.Nested(a_user)})

message = end_point.model('message', {'message': fields.String(required=True, description="success or fail message")})

user_message = end_point.model('user message', {
    'message': fields.String(required=True, description="success or fail message"),
    'user': fields.Nested(a_user)
})


@end_point.route('')
class User(Resource):
    @end_point.expect(new_user)
    @end_point.doc('create a user')
    @end_point.marshal_with(user_message, code=201)
    def post(self):
        data = end_point.payload
        user.add(
            data['username'],
            data['first_name'],
            data['last_name'],
            data['password'],
            data['email'],
        )
        return {
            'message': 'success',
            'user': user.get(user.username)
            }, 201

    @end_point.doc('read all users')
    @end_point.marshal_with(users, code=200)
    def get(self):
        if not user.get_all():
            return {'message': 'Sorry no users found',
                    'user': {}
                    }, 404
        return {'message': 'success',
                'users': user.get_all()
                }, 200


@end_point.route('<username>')
class SingleUser(Resource):
    @end_point.expect(username)
    @end_point.doc('read all users')
    @end_point.marshal_with(a_user, code=200)
    def get(self, username):
        if not user.get(username):
            return {'message': 'Sorry this user is not found',
                    'user': {}
                    }, 404
        return {'message': 'success',
                'user': user.get(username)
                }, 200

    @end_point.expect(username, a_user)
    @end_point.doc('update specific user')
    @end_point.marshal_with(user_message, code=200)
    def put(self, username):
        data = end_point.payload
        user.update(username, {'name':data['name'], 'cost':data['cost'], 'amount':data['amount']})
        return {'message': 'success',
                'user': user.get(int(username))
                }, 200

    @end_point.expect(username)
    @end_point.doc('delete specific user')
    @end_point.marshal_with(message, code=200)
    def delete(self, username):
        user.delete(username)
        return {'message': 'success'}, 200
