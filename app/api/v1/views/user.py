from flask_jwt_extended import (
    create_access_token,
    get_raw_jwt
)
from flask_restplus import Resource, Namespace, fields

from ..views import requires_permission
from ..models.user import User as UserModel

blacklist = set()

user = UserModel()

end_point = Namespace('users', description='users resources')

credentials = end_point.model('Credentials', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
})

username = fields.String(description="The users username")

a_user = end_point.model('user', {
    'username': username,
    'first_name': fields.String(required=True, description="The user's first name"),
    'last_name': fields.String(required=True, description="The user's last name"),
    'email': fields.String(required=True, description="The user's email"),
    'role': fields.String(required=True, description="The user's role")
})

new_user = end_point.model('user', {
    'username': username,
    'first_name': fields.String(required=True, description="The user's first name"),
    'last_name': fields.String(required=True, description="The user's last name"),
    'password': fields.String(required=True, description="The user's password"),
    'email': fields.String(required=True, description="The user's email"),
    'role': fields.String(required=True, description="The user's role")
})

users = end_point.model('users', {
    'username': fields.Nested(a_user)
})

message = end_point.model('message', {
    'message': fields.String(required=True, description="success or fail message")
})

user_message = end_point.model('user message', {
    'message': fields.String(required=True, description="success or fail message"),
    'user': fields.Nested(a_user, skip_none=True)
})


@end_point.route('')
class User(Resource):
    @end_point.expect(new_user)
    @end_point.doc('create a user')
    @end_point.marshal_with(user_message, code=201)
    def post(self):
        data = end_point.payload
        if not data['username'] and data['first_name'] and data['last_name'] and data['password'] and data['email']:
            return {'message': 'Sorry could not add user'}, 404
        user.add(
            data['username'],
            data['first_name'],
            data['last_name'],
            data['password'],
            data['email'],
            data['role']
        )
        return {
            'message': 'success',
            'user': user.get(user.username)
            }, 201

    @requires_permission('admin')
    @end_point.doc('read all users')
    # @end_point.marshal_with(users, code=200)
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
    @requires_permission('store attendant')
    @end_point.expect(username)
    @end_point.doc('read all users')
    @end_point.marshal_with(user_message , code=200)
    def get(self, username):
        if not user.get(username):
            return {'message': 'Sorry this user is not found',
                    'user': {}
                    }, 404
        return {'message': 'success',
                'user': user.get(username)
                }, 200

    @requires_permission('store attendant')
    @end_point.expect(username, a_user)
    @end_point.doc('update specific user')
    @end_point.marshal_with(user_message, code=200)
    def put(self, username):
        req = end_point.payload
        if not user.get(username):
            return {'message': 'Sorry this user is not found'}, 404
        data = {
            'username': req['username'],
            'first_name': req['first_name'],
            'last_name': req['last_name'],
            'password': req['password'],
            'email': req['email']
        }

        if user.update(username, data):
            return {'message': 'success',
                    'user': user.get(username)
                    }, 200
        else:
            return{
                'message': 'Sorry could not update this user'
            }

    @requires_permission('admin')
    @end_point.expect(username)
    @end_point.doc('delete specific user')
    @end_point.marshal_with(message, code=200)
    def delete(self, username):
        if not user.get(username):
            return {'message': 'Sorry this user is not found'}, 404
        if user.delete(username):
            return {'message': 'success'}, 200
        else:
            return{
                'message': 'Sorry could not delete this user'
            }, 205


@end_point.route('login/')
class Login(Resource):
    @end_point.expect(credentials)
    @end_point.doc('login a user')
    def post(self):
        data = end_point.payload
        if not data:
            return {"message": 'Could not sing in unknown user'}, 400
        username = str.strip(data.get('username'))
        password = str.strip(data.get('password'))
        if not username and password:
            return {"message": "Username or password missing"}, 206
        if user.sign_in(username, password):
            return {
                'token': str(create_access_token(identity=username)),
                'message': 'Login successful!'
            }, 200
        return {"message": 'Could not sing in user'}, 401


@end_point.header('Authorization: Bearer', 'JWT TOKEN', required=True)
@end_point.route('logout/')
class Logout(Resource):
    @requires_permission('store attendant')
    def post(self):
        json_token_id = get_raw_jwt()['jti']
        blacklist.add(json_token_id)
        if json_token_id in blacklist:
            return {'message': 'Logged out successfully'}, 200
        else:
            return {'message': 'Could not log out'}, 205
