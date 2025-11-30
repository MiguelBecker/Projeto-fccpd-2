# Desafio 4 — Microsserviços Independentes

## Objetivo

Criar dois microsserviços independentes que se comunicam via HTTP. O Microsserviço A fornece uma lista de usuários em formato JSON, enquanto o Microsserviço B consome esses dados e retorna uma resposta combinada. Cada microsserviço possui seu próprio Dockerfile e pode ser executado individualmente ou via docker-compose.

## Arquitetura do Projeto

desafio4/
├── ms_a/
│   ├── app.py
│   └── Dockerfile
├── ms_b/
│   ├── app.py
│   └── Dockerfile
└── docker-compose.yml

Microsserviços:

- ms_a: fornece dados de usuários
- ms_b: consome ms_a e gera uma descrição formatada

A comunicação ocorre via rede interna criada automaticamente pelo docker-compose.

## Microsserviço A

Fornece a rota /users retornando uma lista JSON.

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/users")
def users():
    return jsonify([
        {"id": 1, "name": "Alice", "active_since": "2022-01-01"},
        {"id": 2, "name": "Bob", "active_since": "2023-05-10"}
    ])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
```

## Dockerfile do Microsserviço A

```
FROM python:3.11-slim
WORKDIR /app
RUN pip install flask
COPY app.py .
EXPOSE 5001
CMD ["python", "app.py"]

```

## Microsserviço B

Consome o microsserviço A pela URL interna e gera descrições dos usuários.

```
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

```

## Dockerfile do Microsserviço B

```
FROM python:3.11-slim
WORKDIR /app
RUN pip install flask requests
COPY app.py .
EXPOSE 5002
CMD ["python", "app.py"]

```

## docker-compose.yml

```
version: "3.9"

services:
  ms_a:
    build: ./ms_a
    container_name: ms_a
    ports:
      - "5001:5001"

  ms_b:
    build: ./ms_b
    container_name: ms_b
    environment:
      SERVICE_A_URL: http://ms_a:5001
    ports:
      - "5002:5002"
    depends_on:
      - ms_a

```


## Como Executar

Para iniciar ambos os microsserviços:
**docker-compose up --build**

Testar o serviço A:
**http://localhost:5001/users**

Testar o serviço B:
**http://localhost:5002/users/summary**

## Conclusão

Os dois microsserviços funcionam de forma independente, executam em containers distintos e se comunicam via HTTP. O Microsserviço B consome corretamente a API fornecida pelo Microsserviço A, atendendo aos requisitos do desafio.


<pre class="overflow-visible!" data-start="2581" data-end="2614"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"></div></div></pre>
