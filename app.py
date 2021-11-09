from flask import Flask
from flask import jsonify, request, make_response
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route('/api/getItemDatabase')
def getItem():
    query = "SELECT * from items where items.id=" + request.args.get('id')
    cnx = mysql.connector.connect(user='root', password="", database="")
    cursor = cnx.cursor(dictionary=True)

    cursor.execute(query)

    result = []

    for row in cursor:
        print(row)
        result.append(row)

    cursor.close()
    cnx.close()
    return jsonify(result)

@app.route("/api/getUsers")
def get_users():
    cnx = mysql.connector.connect(user='root', password="cream", database='ims')
    cursor = cnx.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")

    result = []

    for row in cursor:
        result.append(row)

    cursor.close()
    cnx.close()
    return jsonify(result)