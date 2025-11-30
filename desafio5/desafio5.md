# Desafio 5 — Microsserviços com API Gateway

## Objetivo

Criar uma arquitetura com dois microsserviços independentes e um API Gateway responsável por centralizar o acesso às rotas. O microsserviço users fornece dados de usuários, o microsserviço orders fornece dados de pedidos e o gateway expõe endpoints unificados para consulta. Todos os serviços são executados em containers via Docker Compose.

## Arquitetura do Projeto

desafio5/
├── users/
│   ├── app.py
│   └── Dockerfile
├── orders/
│   ├── app.py
│   └── Dockerfile
├── gateway/
│   ├── app.py
│   └── Dockerfile
└── docker-compose.yml

Serviços:

- users: retorna lista de usuários
- orders: retorna lista de pedidos
- gateway: repassa requisições para users e orders

Todos os serviços se comunicam pela rede interna "internal".

## Microsserviço Users

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/users")
def users():
    return jsonify([
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
```

## Dockerfile Users

```
FROM python:3.11-slim
WORKDIR /app
RUN pip install flask
COPY app.py .
EXPOSE 5001
CMD ["python", "app.py"]

```

## Microsserviço Orders

```
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/orders")
def orders():
    return jsonify([
        {"order_id": 101, "user_id": 1, "item": "Notebook"},
        {"order_id": 102, "user_id": 2, "item": "Mouse"}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)

```

## Dockerfile Orders

```
FROM python:3.11-slim
WORKDIR /app
RUN pip install flask
COPY app.py .
EXPOSE 5002
CMD ["python", "app.py"]

```

## API Gateway

```
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

```

## Dockerfile Gateway

```
FROM python:3.11-slim
WORKDIR /app
RUN pip install flask requests
COPY app.py .
EXPOSE 9000
CMD ["python", "app.py"]

```

## docker-compose.yml

```
version: "3.9"

services:

  users:
    build: ./users
    container_name: users
    ports:
      - "5001:5001"
    networks:
      - internal

  orders:
    build: ./orders
    container_name: orders
    ports:
      - "5002:5002"
    networks:
      - internal

  gateway:
    build: ./gateway
    container_name: gateway
    ports:
      - "9000:9000"
    depends_on:
      - users
      - orders
    environment:
      USERS_URL: http://users:5001/users
      ORDERS_URL: http://orders:5002/orders
    networks:
      - internal

networks:
  internal:

```


## Como Executar

1. No diretório do desafio, iniciar os serviços:
   **docker-compose up --build**
2. Acessar os endpoints via API Gateway:

* Consultar usuários:

  [http://localhost:9000/users]()
* Consultar pedidos:

  [http://localhost:9000/orders]()

O gateway repassa as requisições aos microsserviços internos, funcionando como ponto único de entrada.

## Conclusão

O projeto demonstra uma arquitetura de três serviços em containers, com um API Gateway centralizando as chamadas para os microsserviços. A comunicação entre os serviços ocorre corretamente pela rede interna configurada no Docker Compose, atendendo aos requisitos do desafio.
