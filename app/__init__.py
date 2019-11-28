from flask import Flask, jsonify
from flask import request
from flask_jwt import JWT, jwt_required
from flask_api import status
from app.inventory_demand import transform_data, train_model
from app.models import User
from passlib.hash import pbkdf2_sha256
from flask_cors import CORS
from app.database import init_db, shutdown_db_session
import pandas as pd
import io
import json
from os import environ
app = Flask(__name__)
CORS(app)

@app.teardown_appcontext
def shutdown_session(exception=None):
    shutdown_db_session()

init_db()

@app.route('/api/checkToken', methods=['POST'])
@jwt_required()
def check_token():
    return "SUCCESS", status.HTTP_202_ACCEPTED

@app.route("/api/inventory-demand/data-transformation", methods=['POST'])
def inventory_demand_training():
    content = request.get_json()
    df = pd.io.json.json_normalize(content, 'data')
    months_to_predict = content['monthsToPredict']
    return transform_data(df, months_to_predict)


# @app.route("/api/inventory-demand/model-training", methods=['POST'])
# def inventory_demand_training():
#     content = request.get_json()
#     df = pd.io.json.json_normalize(content, 'data')
#     return train_model(df)


@app.route("/")
def initial():
    print('hi')
    return jsonify({'testing': ["Hello from cross-entropy-services"]})


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and pbkdf2_sha256.verify(password, user.password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)

app.config['SECRET_KEY'] = environ.get('JWT_SECRET_KEY')
jwt = JWT(app, authenticate, identity)
