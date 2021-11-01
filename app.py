from flask import Flask
from flask import jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/api/getItems")
def get_items():
    items = {
        "description": "Bolt",
        "quantity": 8,
        "url": "https://google.com/"
    }
    return jsonify(items)