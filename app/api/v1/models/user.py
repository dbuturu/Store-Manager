from werkzeug.security import generate_password_hash, check_password_hash

users = {}

class User:
    def __init__(self):
        self.users = users
        self.username = ''
        self.first_name = ''
        self.last_name = ''
        self.password = ''
        self.email = ''
        self.role = ''

    def add(self, username, first_name, last_name, password, email, role):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password)
        self.email = email
        self.role = role
        self.users[self.username] = {
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'password': self.password,
            'email': self.email,
            'role': self.role
        }

    def sign_in(self, username: str, password: str):
        if not self.users.get(username):
            return False
        user = self.users[username]
        return check_password_hash(
            user['password'],
            password
        )

    def get(self, username: str):
        return self.users.get(username)

    def get_all(self):
        return self.users

    def update(self, username, user):
        if username:
            self.users.update({user.get('username'): user})
            return self

    def delete(self, username: str):
        if username:
            self.users.pop(username)
            return self
