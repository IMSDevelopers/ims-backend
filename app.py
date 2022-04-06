from flask import Flask
from flask import jsonify, request, make_response
from flask_cors import CORS
import mysql.connector

# imports for AWS
import boto3
from config import S3_BUCKET, S3_KEY, S3_SECRET_ACCESS_KEY
import secrets

# Create the flask app
app = Flask(__name__)
CORS(app)

USERNAME = "admin"
PASSWORD = "admin123"
HOST = "capstonetest-db.cogzcve8vrzk.us-east-1.rds.amazonaws.com"
DATABASE = "ims"

# AWS S3 CLIENT
location = "us-west-1"
s3 = boto3.client(
    's3',
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY)


#########################################
#                ITEMS                  #
#########################################

# Get items
@app.route('/api/getItems')
def get_items():
    try:
        cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host=HOST, database=DATABASE)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM items")

        result = []

        for row in cursor:
            result.append(row)

        cursor.close()
        cnx.close()
        return jsonify(result)
    except:
        return "Failed to get items!"

# Get an item by input
@app.route('/api/getItem/<id>')
def get_item(id):
    try:
        item_id = id
        query = "SELECT * FROM items WHERE items.id={}".format(item_id)
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
    except:
        return "Failed to get item!"

# Post an Item
@app.route("/api/postItem", methods=['POST'])
def post_item():
    try:
        cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host=HOST, database=DATABASE)
        cursor = cnx.cursor(dictionary=True)

        rq = request.get_json()
        query = ("INSERT INTO items (name, quantity, description, url_image) VALUES (\"{}\", {}, \"{}\", \"{}\")".format(
            rq["name"], rq["quantity"], rq["description"], rq["url_image"]))
        cursor.execute(query)

        cnx.commit()
        cursor.close()
        cnx.close()

        return "Item inserted: name: {}, quantity: {}".format(rq["name"], rq["quantity"])
    except:
        return "Add item failed!"

# Delete item
@app.route('/api/deleteItem/<id>')
def delete_item(id):
    try:
        item_id = id
        cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host=HOST, database=DATABASE)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("DELETE FROM items WHERE items.id={}".format(item_id))

        cnx.commit()
        cursor.close()
        cnx.close()
        
        return "Deleted item: item_id: {}".format(item_id)
    except:
        return "Delete item failed!"

# Edit item
@app.route('/api/editItem/<id>', methods=['PUT'])
def edit_item(id):
    try:
        item_id = id
        cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host=HOST, database=DATABASE)
        cursor = cnx.cursor(dictionary=True)
        
        rq = request.get_json()
        
        cursor.execute("UPDATE items SET name = \"{}\", quantity = {}, description = \"{}\", url_image = \"{}\" WHERE id = {}".format(
            rq["name"], rq["quantity"], rq["description"], rq["url_image"], item_id))

        cnx.commit()
        cursor.close()
        cnx.close()

        return "Success!"
    except:
        return "Edit item failed!"

#########################################
#                ORDERS                 #
#########################################

# Post an Order
@app.route("/api/postOrder", methods=['POST'])
def post_order():
    try:
        cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host=HOST, database=DATABASE)
        cursor = cnx.cursor(dictionary=True)

        rq = request.get_json()
        query = ("INSERT INTO orders (order_id, item_id, num_ordered, student_id, order_status) VALUES ({}, {}, {}, \"{}\", \"{}\")".format(
            rq["order_id"], rq["item_id"], rq["num_ordered"], rq["student_id"], rq["order_status"]))
        cursor.execute(query)

        cnx.commit()
        cursor.close()
        cnx.close()

        return "Order inserted: order_id: {}, item_id: {}, num_ordered: {}, student_id: {}".format(
            rq["order_id"], rq["item_id"], rq["num_ordered"], rq["student_id"])
    except:
        return "Post order failed!"

# Get orders
@app.route('/api/getOrders')
def get_orders():
    try:
        cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host=HOST, database=DATABASE)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT orders.order_id, orders.order_status, orders.student_id, \
                        items.id as item_id, items.name, items.description, \
                        items.url_image, orders.num_ordered \
                        FROM orders, items WHERE orders.item_id = items.id;")

        initial = [row for row in cursor]

        result = []
        for row in initial:
            order = dict(order_id=row["order_id"], order_status=row["order_status"], student_id=row["student_id"], items=[])
            result_order_ids = [r["order_id"] for r in result]
            if row["order_id"] not in result_order_ids:
                result.append(order)
            

        for row in initial:
            order_id = row["order_id"]
            for order in result:
                if order["order_id"] == order_id: # this is the order, insert items into it
                    item = dict(item_id=row["item_id"], item_name=row["name"], \
                                description=row["description"], url_image=row["url_image"], num_ordered=row["num_ordered"])
                    order["items"].append(item)
                    break

        print(result)

        cursor.close()
        cnx.close()
        return jsonify(result)
    except:
        return "Failed to get orders!"

# Delete order
@app.route('/api/deleteOrder/<id>')
def delete_order(id):
    try:
        order_id = id
        cnx = mysql.connector.connect(user=USERNAME, password=PASSWORD, host=HOST, database=DATABASE)
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("DELETE FROM orders WHERE orders.order_id={}".format(order_id))

        cnx.commit()
        cursor.close()
        cnx.close()
        
        return "Deleted order: order_id: {}".format(order_id)
    except:
        return "Delete order failed!"

#########################################
#                  S3                   #
#########################################

@app.route('/api/upload', methods=['POST'])
def upload():
    print("Accessed")
    random_code = secrets.token_bytes(12) #Generate 12 random bytes
    hex_code = random_code.hex() 
    
    file = request.files['file']
    print(file)
    try:
        s3.upload_fileobj(
            file,
            S3_BUCKET,
            hex_code,
            ExtraArgs={
                "ACL": "bucket-owner-full-control",
                "ContentType": "multipart/form-data"    #Set appropriate content type as per the file
            }
        )
        url = "https://%s.s3.amazonaws.com/%s" % (S3_BUCKET, hex_code)
        print(url) #this url needs to be saved on the database

    except Exception as e:
        print("Something Happened: ", e)
        return e
    return  url, 200
    





