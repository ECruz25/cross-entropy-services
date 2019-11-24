from flask_jwt import JWT
from jwtauth import app
from jwtauth.models import User
from passlib.hash import pbkdf2_sha256
from os import environ

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    print(user)
    if user and pbkdf2_sha256.verify(password, user.password):
        print(user)
        return user


def identity(payload):
    user_id = payload['identity']
    print(User.query.get(user_id))
    return User.query.get(user_id)


app.config['SECRET_KEY'] = environ.get('JWT_SECRET_KEY')
jwt = JWT(app, authenticate, identity)