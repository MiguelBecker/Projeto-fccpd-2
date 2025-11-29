import sqlite3
import os
from datetime import datetime

DB_PATH = "/data/app.db"

def init_db():
    os.makedirs("/data", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    msg = f"Registro criado em {datetime.utcnow().isoformat()}"
    cur.execute("INSERT INTO logs (message, created_at) VALUES (?, ?)", (msg, datetime.utcnow().isoformat()))

    conn.commit()

    print("Registros atuais no banco:")
    for row in cur.execute("SELECT * FROM logs"):
        print(row)

    conn.close()

if __name__ == "__main__":
    init_db()
