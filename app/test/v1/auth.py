import json

def add_user(client):
    user_login = client.post(
        '/api/v1/users/',
        data=json.dumps(
            {
                "username": "user",
                "first_name": "store",
                "last_name": "attendant",
                "password": "password",
                "email": "user@email.com",
                "role": "store attendant"
            }
        ),
        content_type='application/json'
    )
    admin_login = client.post(
        '/api/v1/users/',
        data=json.dumps(
            {
                "username": "admin",
                "first_name": "store",
                "last_name": "admin",
                "password": "password",
                "email": "admin@email.com",
                "role": "admin"
            }
        ),
        content_type='application/json'
    )
    return {
        'user_login': user_login,
        'admin_login': admin_login
    }

def login_users(client):
    user_login = client.post(
        '/api/v1/users/login/',
        data=json.dumps({
            "username": "user",
            "password": "password"
        }),
        content_type='application/json'
    )
    admin_login = client.post(
        "/api/v1/users/login",
        data=json.dumps({
            'username': 'admin',
            'password': 'password'
        }), content_type='application/json'
    )
    user_data = json.loads(user_login.data)
    admin_data = json.loads(admin_login.data)
    return {
        'user_token': user_data["token"],
        'admin_token': admin_data["token"]
    }
