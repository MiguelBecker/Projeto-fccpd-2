# Desafio 3 — Docker Compose Orquestrando Serviços

## Objetivo

Demonstrar o uso do Docker Compose para orquestrar múltiplos serviços interdependentes. O projeto contém três serviços: uma aplicação web em Flask, um banco de dados PostgreSQL e um serviço de cache Redis. O Compose configura as dependências, rede interna e variáveis de ambiente para permitir a comunicação entre os serviços.

## Arquitetura do Projeto

desafio3/
├── web/
│   ├── app.py
│   └── Dockerfile
└── docker-compose.yml

Serviços:

- web: aplicação Python Flask, porta 8000
- db: banco PostgreSQL armazenando dados em volume persistente
- cache: serviço Redis utilizado como contador

Todos os serviços utilizam uma rede interna chamada "internal".

## Serviço Web (Flask)

O serviço web realiza duas operações principais:

1. Incrementa um contador armazenado no Redis.
2. Registra cada visita no banco PostgreSQL, criando a tabela "visits" caso ela não exista.

Conteúdo de app.py:

```python
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
```

## Dockerfile do serviço Web

```
FROM python:3.11-slim
WORKDIR /app
RUN pip install flask psycopg2-binary redis
COPY app.py .
EXPOSE 8000
CMD ["python", "app.py"]
```


## docker-compose.yml

```
version: "3.9"

services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: appuser
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: appdb
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - internal

  cache:
    image: redis:7
    networks:
      - internal

  web:
    build: ./web
    ports:
      - "8000:8000"
    environment:
      DATABASE_HOST: db
      DATABASE_NAME: appdb
      DATABASE_USER: appuser
      DATABASE_PASSWORD: secret
      REDIS_HOST: cache
    depends_on:
      - db
      - cache
    networks:
      - internal

networks:
  internal:

volumes:
  db-data:

```


## Como Executar

1. No diretório desafio3, executar:
   **docker-compose up --build**
2. Acessar a aplicação:
   **http://localhost:8000**
3. A cada atualização da página:

* O contador armazenado no Redis é incrementado.
* Uma nova linha é inserida na tabela "visits" do PostgreSQL.

## Conclusão

O projeto demonstra o uso do Docker Compose para orquestrar três serviços interligados, configurando rede interna, variáveis de ambiente e dependências entre eles. A comunicação entre os serviços funciona corretamente e a aplicação atende aos requisitos do desafio.
