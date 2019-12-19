from flask import Flask, jsonify
from flask import request
from flask_jwt import JWT, jwt_required
from flask_api import status
from app.inventory_demand import transform_data, train_model
from app.models import User
from passlib.hash import pbkdf2_sha256
from flask_cors import CORS
from app.database import init_db, shutdown_db_session, db_session, save_model_to_db, load_saved_model_from_db, load_models_by_user
from app.models import User
from passlib.hash import pbkdf2_sha256
import pandas as pd
import numpy as np
import io
import json
from os import environ
app = Flask(__name__)
CORS(app)

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

@app.teardown_appcontext
def shutdown_session(exception=None):
    shutdown_db_session()

init_db()

def useradd(username, password):
    db_session.add(User(username, pbkdf2_sha256.hash(password)))
    db_session.commit()

@app.route('/api/checkToken', methods=['POST'])
@jwt_required()
def check_token():
    return "SUCCESS", status.HTTP_202_ACCEPTED

@app.route("/api/create-user", methods=['POST'])
def create_user():
    content = request.get_json()
    print(content['username'])
    useradd(content['username'], content['password'])
    return "SUCCESS", status.HTTP_202_ACCEPTED
    
@app.route("/api/inventory-demand/data-transformation", methods=['POST'])
def inventory_demand_data_transformation():
    content = request.get_json()
    df = pd.io.json.json_normalize(content, 'data')
    months_to_predict = content['monthsToPredict']
    transformed_data = transform_data(df, months_to_predict)
    transformed_data['model_details'] = { 'months': months_to_predict }
    return json.dumps(transformed_data, cls=NumpyEncoder), status.HTTP_200_OK

@app.route("/api/inventory-demand/model-training", methods=['POST'])
def inventory_demand_training():
    content = request.get_json()
    df = pd.io.json.json_normalize(content, 'data')
    months_to_predict = content['monthsToPredict']
    user_id = content['user']
    transformed_data = transform_data(df, months_to_predict)
    model_details = { 'months_to_predict': months_to_predict }
    
    trained_model = train_model(transformed_data['X_train_series'], transformed_data['X_valid_series'], transformed_data['Y_train'], transformed_data['Y_valid'])
    save_model_to_db(model=trained_model, model_type='Demanda de inventario', user=user_id, model_details=model_details)
    return "SUCCESS", status.HTTP_202_ACCEPTED

@app.route("/api/trained_models/<user_id>", methods=['GET'])
def get_trained_models(user_id):
    trained_models = load_models_by_user(user_id) 
    return json.dumps(trained_models, cls=NumpyEncoder)

@app.route("/api")
def initial():
    return jsonify({'testing': ["Hello from cross-entropy-services"]})

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and pbkdf2_sha256.verify(password, user.password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)

app.config['SECRET_KEY'] = "holaaa"
jwt = JWT(app, authenticate, identity)

if __name__ == '__main__':
    app.run(debug=True)