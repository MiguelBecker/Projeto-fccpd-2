from flask import Flask, jsonify
import os
import psycopg2
import redis

app = Flask(__name__)

r = redis.Redis(host=os.getenv("REDIS_HOST", "cache"), port=6379, db=0)

db_conn = psycopg2.connect(
    host=os.getenv("DATABASE_HOST", "db"),
    dbname=os.getenv("DATABASE_NAME", "appdb"),
    user=os.getenv("DATABASE_USER", "appuser"),
    password=os.getenv("DATABASE_PASSWORD", "secret"),
)

@app.route("/")
def index():
    redis_hits = r.incr("hits")

    cur = db_conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id SERIAL PRIMARY KEY,
            info TEXT
        )
    """)
    cur.execute("INSERT INTO visits (info) VALUES (%s)", (f"Visita número {redis_hits}",))
    db_conn.commit()
    cur.close()

    return jsonify({
        "message": "Aplicação Web está funcionando",
        "redis_hits": int(redis_hits),
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
