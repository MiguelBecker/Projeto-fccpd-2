from flask import Flask, jsonify
import requests
import os

app = Flask(__name__)

SERVICE_A_URL = os.getenv("SERVICE_A_URL", "http://ms_a:5001")

@app.route("/users/summary")
def summary():
    response = requests.get(f"{SERVICE_A_URL}/users")
    users = response.json()

    result = [
        {"description": f"Usuário {u['name']} ativo desde {u['active_since']}"}
        for u in users
    ]

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
