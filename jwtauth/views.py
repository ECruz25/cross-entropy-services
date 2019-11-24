from flask_jwt import jwt_required
from jwtauth import app


@app.route('/hello')
@jwt_required()
def hello():
    return 'Hello world!'