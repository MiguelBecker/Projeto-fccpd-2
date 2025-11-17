# Projeto 2

# Desafio 1 — Containers em Rede

## 1. Descrição da solução, arquitetura e decisões técnicas

Este desafio implementa dois containers Docker que se comunicam por meio de uma rede customizada:

- Um container executa um servidor web usando Flask, escutando na porta 8080.
- Um segundo container executa um script em shell que faz requisições HTTP periódicas (via `curl`) para o servidor.
- Ambos os containers são orquestrados com `docker-compose` e conectados a uma rede Docker do tipo `bridge` chamada `minha_rede`.

Decisões técnicas principais:

- Uso de Flask pela simplicidade para expor um endpoint HTTP básico.
- Separação em duas imagens distintas:
  - `Dockerfile.server`: imagem do servidor Flask.
  - `Dockerfile.client`: imagem do cliente que roda um loop com `curl`.
- Uso de nomes de serviço do `docker-compose` (por exemplo, `server`) para resolução de DNS dentro da rede Docker, simplificando o endereço usado pelo cliente: `http://server:8080`.
- Exposição da porta `8080` do servidor para o host, permitindo testes manuais com `curl` ou navegador.

Estrutura de arquivos do desafio (todos dentro do diretório `desafio1/`):

