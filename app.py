from flask import Flask
from flask import jsonify, request, make_response
from flask_cors import CORS
import mysql.connector

#Create the flask app
app = Flask(__name__)
CORS(app)

USERNAME = "root"
PASSWORD = ""
DATABASE = ""

@app.route("/")
def home():
    return "Hello, Flask!"

#Get an item by input
@app.route('/api/getItemById')
def get_item():
    query = "SELECT * FROM items WHERE items.id=" + request.args.get('id')
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, database=DATABASE)
    cursor = cnx.cursor(dictionary=True)

    cursor.execute(query)

    result = []

    for row in cursor:
        print(row)
        result.append(row)

    cursor.close()
    cnx.close()
    return jsonify(result)


#Get items
@app.route('/api/getItems')
def get_items():
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, database=DATABASE)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items")

    result = []

    for row in cursor:
        result.append(row)

    cursor.close()
    cnx.close()
    return jsonify(result)

#Post an Item
@app.route('/api/postItem')
def post_item():
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, database=DATABASE)
    cursor = cnx.cursor(dictionary=True)

    request_data =  request.data()
    #request.get_json()

    print(request_data)
    cursor.close()
    cnx.close()
#Enter data in mysql
    return jsonify(request_data)

#Get users
@app.route("/api/getUsers")
def get_users():
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, database=DATABASE)
    cursor = cnx.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")

    result = []

    for row in cursor:
        result.append(row)

    cursor.close()
    cnx.close()
    return jsonify(result)
