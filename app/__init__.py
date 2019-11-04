from app.inventory_demand import transform_data, train_model
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS
import pandas as pd
import io
import json
app = Flask(__name__)
CORS(app)


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
def hello():
    return jsonify({'testing': ["Hello from cross-entropy-services"]})
