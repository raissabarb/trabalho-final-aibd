# Trabalho Final AIBD - Redis Flask Application

Esta é uma aplicação Flask que se conecta a um banco de dados Redis para armazenar e recuperar dados. A aplicação inclui endpoints para definir e obter valores, visualizar todos os dados armazenados, e listar estudantes.

## Estrutura do Projeto

- **app.py**: Código principal da aplicação Flask.
- **Dockerfile**: Arquivo de configuração para construir a imagem Docker da aplicação.
- **docker-compose.yaml**: Arquivo de configuração para orquestrar os serviços Docker (Redis e aplicação Flask).
- **requirements.txt**: Arquivo de requisitos para instalar as dependências da aplicação.

## Pré-requisitos

Antes de começar, é necessário que o Docker e o Docker Compose estejam instalados na máquina local. A instalação do Docker e Docker Compose  pode ser feita seguindo as instruções [neste link](https://docs.docker.com/get-docker/).

## Configuração

1. **Clone o repositório**

   ```sh
   git clone <URL_DO_REPOSITORIO>
   cd <NOME_DO_REPOSITORIO>
