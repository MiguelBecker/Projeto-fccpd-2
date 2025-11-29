# Desafio 1 — Containers em Rede

## Objetivo

Demonstrar a comunicação entre dois containers Docker conectados por uma rede customizada. O projeto contém um servidor Flask que responde na porta 8080 e um cliente que realiza requisições HTTP periódicas ao servidor utilizando curl.

## Arquitetura do Projeto

O diretório contém os seguintes arquivos:

- app.py: servidor Flask que responde na porta 8080
- client.sh: script que faz requisições contínuas ao servidor
- Dockerfile.server: imagem Docker do servidor
- Dockerfile.client: imagem Docker do cliente
- docker-compose.yml: orquestração da rede e containers

## Servidor (Flask)

O servidor oferece um endpoint simples em "/", retornando uma mensagem de confirmação. Código:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Servidor Flask ativo"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

## Cliente (curl em loop)

O cliente envia uma requisição a cada 3 segundos:

```echo
while true; do
    echo "Requisitando servidor"
    curl http://server:8080
    echo ""
    sleep 3
done
```

## Dockerfile do Servidor

```
FROM python:3.11-slim
WORKDIR /app
RUN pip install flask
COPY app.py .
EXPOSE 8080
CMD ["python", "app.py"]
```

## Dockerfile do Cliente

```
FROM alpine:3.20
RUN apk add --no-cache curl
WORKDIR /app
COPY client.sh .
RUN chmod +x client.sh
CMD ["./client.sh"]

```

## docker-compose.yml

```
version: "3.9"

services:
  server:
    build:
      context: .
      dockerfile: Dockerfile.server
    container_name: server
    ports:
      - "8080:8080"
    networks:
      - desafio1-net

  client:
    build:
      context: .
      dockerfile: Dockerfile.client
    container_name: client
    depends_on:
      - server
    networks:
      - desafio1-net

networks:
  desafio1-net:
    driver: bridge

```

<pre class="overflow-visible!" data-start="1527" data-end="1662"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"></div></div></pre>

## Como Executar

Executar no diretório do desafio:

<pre class="overflow-visible!" data-start="2159" data-end="2192"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre!"><span><span>docker-compose up </span><span>--build</span><span>
</span></span></code></div></div></pre>

O servidor iniciará na porta 8080 e o cliente enviará requisições periódicas. A comunicação entre containers ocorrerá pela rede interna desafio1-net, utilizando o hostname "server".

## Funcionamento

O servidor imprime logs de acesso HTTP. O cliente imprime o texto "Servidor Flask ativo" a cada requisição enviada. Ambos os containers ficam conectados através da rede Docker customizada, demonstrando comunicação contínua entre serviços.

## Decisões Técnicas

* Flask foi utilizado pela simplicidade ao expor um endpoint HTTP.
* Alpine Linux foi usado para obter uma imagem leve no cliente.
* docker-compose foi escolhido para facilitar a orquestração dos containers.
* A rede personalizada permite que o cliente acesse o servidor usando o hostname interno.

`<pre class="overflow-visible!" data-start="1374" data-end="1499"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary">``<div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2">``<div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"></div>``</div></div>``<div class="overflow-y-auto p-4" dir="ltr"></div>``</div>`</pr
