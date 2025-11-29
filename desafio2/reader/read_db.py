import sqlite3

DB_PATH = "/data/app.db"

def read_all():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    print("Lendo registros existentes:")
    for row in cur.execute("SELECT * FROM logs"):
        print(row)

    conn.close()

if __name__ == "__main__":
    read_all()
