from flask import Flask
from flask import jsonify, request, make_response
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

try:
  cnx = mysql.connector.connect(user='root', password='root',  host='127.0.0.1', database='ims_database')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)


@app.route('/api/getUser')
def index():
    cursor = cnx.cursor()
    cursor.execute("SELECT * from user where user.id=1")
    data = cursor.fetchall()
    return str(data)


# @app.route('/api/postItem', methods = ['POST'])
# def addItem():
#     data = request.get_json()
#     details = request.form
#     amount = details['amount']
#     description = details['description']
#     img = details['image_url']
#     filterId = details['id_filters']
#     name = details['name']
#     cursor = mysql.connection.cursor()
#     cursor.execute("INSERT INTO items(amount, description, image_url, id_filters, name) VALUES (%s, %s, %s, %s, %s)", (amount, description, img, filterId, name))
#     mysql.connection.commit()
#     cursor.close()
#     return 'success'


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
