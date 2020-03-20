class Config(object):
    JWT_SECRET_KEY = 'holaaa'
    JWT_ALGORITHM = 'HS256'
    JWT_AUTH_ENDPOINT = 'jwt'
    JWT_AUTH_USERNAME_KEY = 'email'
    JWT_AUTH_PASSWORD_KEY = 'password'