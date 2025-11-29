# Desafio 2 — Volumes e Persistência

## Objetivo

Demonstrar a persistência de dados utilizando volumes Docker. A solução consiste em um container que cria e atualiza um banco SQLite, salvando-o em um volume que permanece mesmo após o container ser removido. Um segundo container opcional lê os dados persistidos.

## Arquitetura do Projeto

O diretório possui a seguinte estrutura:

desafio2/
├── db/
│   ├── init_db.py
│   └── Dockerfile
├── reader/
│   ├── read_db.py
│   └── Dockerfile
└── docker-compose.yml

O volume utilizado chama-se "desafio2-data" e é montado no diretório /data de ambos os containers.

## Funcionamento do Container db

O container responsável pela escrita executa o script init_db.py, que realiza as seguintes ações:

1. Cria o diretório /data (caso não exista).
2. Cria o banco SQLite app.db no volume.
3. Cria a tabela logs se ela não existir.
4. Insere um novo registro a cada execução.
5. Exibe todos os registros existentes, permitindo verificar se os dados persistem entre execuções.

Conteúdo do init_db.py:

```python
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
```

## Funcionamento do Container reader (opcional)

Este container lê o banco existente no volume e exibe todos os registros, provando que eles persistem.

Conteúdo de read_db.py:

```import
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


```

## Dockerfile do Container db

```
FROM python:3.11-slim
WORKDIR /app
COPY init_db.py .
CMD ["python", "init_db.py"]

```

## Dockerfile do Container reader

```
FROM python:3.11-slim
WORKDIR /app
COPY read_db.py .
CMD ["python", "read_db.py"]

```

## docker-compose.yml

```
version: "3.9"

services:
  db:
    build: ./db
    volumes:
      - desafio2-data:/data

  reader:
    build: ./reader
    volumes:
      - desafio2-data:/data

volumes:
  desafio2-data:

```


## Como Executar

1. Executar o container que insere dados:
   **docker-compose run db**
2. Executar novamente para verificar a persistência:
   **docker-compose run db**
3. Executar o container leitor:
   **docker-compose run reader**
4. Verificar que o volume permanece mesmo após remover containers:
   **docker ps -a
   docker rm `<containers>`
   docker volume ls**


## Conclusão

O projeto demonstra que os dados armazenados no volume Docker persistem mesmo após a remoção do container, atendendo aos requisitos do desafio e permitindo visualização clara da persistência tanto na execução repetida do container db quanto na leitura realizada pelo container reader.
