from flask import Flask
from flask import request
from flask_cors import CORS
import pandas as pd
import io
import json
app = Flask(__name__, static_folder="../../cross-entropy-client/build/static")
CORS(app)
from app.inventory_demand import train

@app.route("/api/inventory-demand", methods=['POST'])
def inventory_demand_training():
    content = request.get_json()
    df = pd.io.json.json_normalize(content, 'data')
    return train(df)

@app.route("/api")
def hello():
    return "HELLO"