from flask import Flask
from flask import jsonify, request, make_response
from flask_cors import CORS
import mysql.connector

# Create the flask app
app = Flask(__name__)
CORS(app)

USERNAME = ""
PASSWORD = ""
HOST = "capstonetest-db.cogzcve8vrzk.us-east-1.rds.amazonaws.com"
DATABASE = "ims"

@app.route("/")
def home():
    return "Hello, Flask!"

# Get an item by input
@app.route('/api/getItemById')
def get_item():
    query = "SELECT * FROM items WHERE items.id=" + request.args.get('id')
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host=HOST, database=DATABASE)
    cursor = cnx.cursor(dictionary=True)

    cursor.execute(query)

    result = []

    for row in cursor:
        print(row)
        result.append(row)

    cursor.close()
    cnx.close()
    return jsonify(result)


# Get items
@app.route('/api/getItems')
def get_items():
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host=HOST, database=DATABASE)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items")

    result = []

    for row in cursor:
        result.append(row)

    cursor.close()
    cnx.close()
    return jsonify(result)

# Post an Item
@app.route("/api/postItem", methods=['POST'])
def post_item():
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host=HOST, database=DATABASE)
    cursor = cnx.cursor(dictionary=True)

    rq = request.form
    query = ("INSERT INTO items (name, quantity, description, url_image) VALUES ({}, {}, {}, {})".format(rq["name"], rq["quantity"], rq["description"], rq["url_image"]))
    cursor.execute(query)

    cnx.commit()
    cursor.close()
    cnx.close()

    return "Success!"

# Post an Order
@app.route("/api/postOrder", methods=['POST'])
def post_order():
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host=HOST, database=DATABASE)
    cursor = cnx.cursor(dictionary=True)

    rq = request.form
    query = ("INSERT INTO orders (item_id, num_ordered, student_id) VALUES ({}, {}, {})".format(rq["item_id"], rq["num_ordered"], rq["student_id"]))
    cursor.execute(query)

    cnx.commit()
    cursor.close()
    cnx.close()

    return "Success!"

# Get orders
@app.route('/api/getOrders')
def get_orders():
    cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host=HOST, database=DATABASE)
    cursor = cnx.cursor(dictionary=True)
    cursor.execute("SELECT * FROM orders")

    result = []

    for row in cursor:
        result.append(row)

    cursor.close()
    cnx.close()
    return jsonify(result)
