# PI-ARNOT-SUPREMO

## Visão Geral

PI-ARNOT-SUPREMO é uma aplicação web baseada em Flask, projetada para gerenciar registros de acesso, armazenando-os em um banco de dados SQLite. A aplicação fornece uma API RESTful para receber e recuperar registros de acesso, com mecanismos robustos de log e tratamento de erros.


O código existente na placa Raspberry Pi Pico W irá fazer requisições através da rota POST "/receber_dados" criada para a API Flask e os enviará em um formato JSON. A outra rota criada GET "/registros_acesso" será consumida pelo meu front-end e irá receber os registros no formato JSON.



## Funcionalidades

- **API RESTful**: Dois endpoints para receber e recuperar registros de acesso.
- **Banco de Dados SQLite**: Armazena registros de acesso localmente.
- **Log**: Logs de informações, avisos e erros em arquivos separados e no console.
- **CORS Habilitado**: Permite requisições cross-origin de qualquer domínio.

## Requisitos
- Python 3.8 ou superior
- Flask
- Flask-CORS
- SQLite3


## Instruções de Configuração
Usando Docker

1. Construa a imagem Docker:
    - docker-compose build

2. Execute o container Docker:
    - docker-compose up


## Configuração Manual
1. Clone o repositório:

   - git clone https://github.com/seu-usuario/PI-ARNOT-SUPREMO.git
   - cd PI-ARNOT-SUPREMO/PI-BACK-END

2. Instale as dependências:

    - Usando Pipenv:

        - pipenv install
        - pipenv shell
    - Usando pip:

        - pip install -r requirements.txt


3. Execute a aplicação Flask:

    - python app.py


## Endpoints da API
POST /receber_dados
Recebe registros de acesso de um dispositivo.

- URL: /receber_dados
- Método: POST
- Content-Type: application/json
- Corpo da Requisição:
    - json
        {
        "id_cartao": "integer",
        "nome_pessoa": "string",
        "horario": "datetime",
        "status_acesso": "string"
        }

- Respostas:
    - 200 OK: Dados recebidos e inseridos com sucesso.
    - 400 Bad Request: Dados incompletos recebidos.
    - 500 Internal Server Error: Erro ao processar os dados.


GET /registros_acesso
Retorna todos os registros de acesso em formato JSON.

- URL: /registros_acesso
- Método: GET
- Respostas:
    - 200 OK: Registros obtidos com sucesso.
    - 500 Internal Server Error: Erro ao obter registros.

## Log
A aplicação realiza logs das informações no diretório logs:

- info.log: Registra mensagens informativas.
- error.log: Registra mensagens de erro.
- Console: Registra todas as mensagens no console para monitoramento em tempo real.


## Banco de Dados
A aplicação usa um banco de dados SQLite (database.db) para armazenar registros de acesso. O esquema do banco de dados é criado automaticamente se ainda não existir.

Esquema
- Tabela: registros_acesso
    - id (INTEGER, PRIMARY KEY, AUTOINCREMENT)
    - id_cartao (INTEGER)
    - nome_pessoa (TEXT)
    - horario (DATETIME)
    - status_acesso (TEXT)


## Contribuindo
Contribuições são bem-vindas! Por favor, faça um fork do repositório e envie um pull request.

