from app.inventory_demand import train
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS
import pandas as pd
import io
import json
app = Flask(__name__)
CORS(app)


@app.route("/api/inventory-demand", methods=['POST'])
def inventory_demand_training():
    content = request.get_json()
    df = pd.io.json.json_normalize(content, 'data')
    return train(df)


@app.route("/api")
def hello():
    return jsonify({'movies': ["Hola"]})
