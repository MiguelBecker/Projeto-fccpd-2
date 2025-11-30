from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

USERS_URL = os.getenv("USERS_URL", "http://users:5001/users")
ORDERS_URL = os.getenv("ORDERS_URL", "http://orders:5002/orders")

@app.route("/users")
def get_users():
    response = requests.get(USERS_URL)
    return jsonify(response.json())

@app.route("/orders")
def get_orders():
    response = requests.get(ORDERS_URL)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000)
