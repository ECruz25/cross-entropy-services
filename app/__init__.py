import json

import numpy as np
import pandas as pd
from flask import Flask, jsonify
from flask import request
from flask_api import status
from flask_cors import CORS
from flask_jwt import JWT, jwt_required
from passlib.hash import pbkdf2_sha256

from app.database import init_db, shutdown_db_session, db_session, save_model_to_db, load_saved_model_from_db, \
    load_models_by_user
from app.inventory_demand import transform_data, train_model, load_sample_data
from app.models import User
from app.models import User, PaymentTransaction, Company

app = Flask(__name__)
CORS(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    shutdown_db_session()


init_db()

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def add_user(username, password, company_id, user_type):
    db_session.add(User(username, pbkdf2_sha256.hash(password), company_id=company_id, user_type=user_type))
    db_session.commit()


@app.route('/api/v1/sign-up', methods=['POST'])
def sign_up():
    content = request.get_json()
    print(content)
    db_session.add(Company(content['email'], content['companyName'], pbkdf2_sha256.hash(content['password']),
                           content['countryId'], content['country']))
    db_session.commit()
    company = Company.query.filter_by(email=content['email']).first()
    add_user(content['email'], content['password'], company.id, user_type="Owner")
    return "SUCCESS", status.HTTP_202_ACCEPTED



@app.route('/api/v1/checkToken', methods=['POST'])
@jwt_required()
def check_token():
    return "SUCCESS", status.HTTP_202_ACCEPTED


@app.route('/api/v1/get-user', methods=['POST'])
def check_user():
    content = request.get_json()
    user = User.query.filter_by(email=content['email']).first()
    return user.__getitem__(), status.HTTP_202_ACCEPTED

@app.route('/api/v1/get-users', methods=['POST'])
def get_users():
    content = request.get_json()
    users = User.query.filter_by(company_id=content['id']).all()
    t = pd.DataFrame(columns=['email', 'type'])
    for tal in users:
        p = {
            'email': tal.email,
            'type': tal.user_type
        }
        t = t.append(p, ignore_index=True )
    return t.to_json(orient='records'), status.HTTP_202_ACCEPTED

@app.route("/api/v1/create-user", methods=['POST'])
def create_user():
    content = request.get_json()
    add_user(content['email'], content['password'], content['company_id'], content['type'])
    return "SUCCESS", status.HTTP_202_ACCEPTED


### verified


def get_amount_by_user(username):
    transactions = db_session.query(PaymentTransaction).filter_by(username=username).all()
    amounts = 0
    for transaction in transactions:
        amounts = amounts + int(transaction.amount)

    return str(amounts)




def add_transaction(username, payment_id, amount, dollar_amount):
    db_session.add(PaymentTransaction(username, payment_id, amount, dollar_amount))
    db_session.commit()










@app.route("/api/v1/create-transaction", methods=['POST'])
def create_transaction():
    content = request.get_json()
    add_transaction(content['username'],
                    content['paymentId'],
                    content['amount'],
                    content['dollarAmount'])
    return "SUCCESS", status.HTTP_200_OK


@app.route("/api/v1/inventory-demand/data-transformation", methods=['POST'])
def inventory_demand_data_transformation():
    content = request.get_json()
    df = pd.io.json.json_normalize(content, 'data')
    months_to_predict = content['monthsToPredict']
    transformed_data = transform_data(df, months_to_predict)
    transformed_data['model_details'] = {'months': months_to_predict}
    return json.dumps(transformed_data, cls=NumpyEncoder), status.HTTP_200_OK


@app.route("/api/v1/inventory-demand/model-training", methods=['POST'])
def inventory_demand_training():
    content = request.get_json()
    df = pd.io.json.json_normalize(content, 'data')
    months_to_predict = content['monthsToPredict']
    user_id = content['user']
    transformed_data = transform_data(df, months_to_predict)
    model_details = {'months_to_predict': months_to_predict}
    print(content)
    trained_model = train_model(transformed_data['X_train_series'], transformed_data['X_valid_series'],
                                transformed_data['Y_train'], transformed_data['Y_valid'])
    save_model_to_db(model=trained_model, model_type='Demanda de inventario', user=user_id, model_details=model_details)
    return "SUCCESS", status.HTTP_202_ACCEPTED


@app.route("/api/v1/trained_models/<user_id>", methods=['GET'])
def get_trained_models(user_id):
    trained_models = load_models_by_user(user_id)
    return json.dumps(trained_models, cls=NumpyEncoder)


@app.route("/api/v1")
def initial():
    return jsonify({'testing': ["Hello from cross-entropy-services"]})


@app.route('/api/v1/inventory-demand/result/<result_id>')
def load(result_id):
    return json.dumps(load_sample_data(), cls=NumpyEncoder), status.HTTP_200_OK


@app.route('/api/v1/credit-by-user/<username>')
def get_credit_by_user(username):
    return get_amount_by_user(username)


def authenticate(email, password):
    user = User.query.filter_by(email=email).first()
    if user and pbkdf2_sha256.verify(password, user.password):
        return user


def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)


app.config['SECRET_KEY'] = "holaaa"
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
jwt = JWT(app, authenticate, identity)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4400)