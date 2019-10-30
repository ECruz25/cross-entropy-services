from flask import Flask
app = Flask(__name__)
from app.regression import analyze

@app.route("/")
def hello():
    return analyze()