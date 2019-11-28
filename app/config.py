import os

class Config(object):
    JWT_SECRET_KEY = 'test123'
    JWT_ALGORITHM = 'HS256'
    JWT_AUTH_ENDPOINT = 'jwt'
    JWT_AUTH_USERNAME_KEY = 'username'
    JWT_AUTH_PASSWORD_KEY = 'password'