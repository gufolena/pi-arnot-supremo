from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import logging


app = Flask(__name__)
CORS(app)  # Adiciona suporte CORS ao seu aplicativo Flask

# Setup logging
logging.basicConfig(level=logging.INFO)

# Function to connect to the database


def conectar_bd():
    conn = sqlite3.connect('database.db')
    return conn

# Route to receive data from the device


@app.route('/receber_dados', methods=['POST'])
def receber_dados():
    if request.method == 'POST':
        try:
            dados = request.json  # assumes that the data is sent as JSON
            id_cartao = dados.get('id_cartao')
            nome_pessoa = dados.get('nome_pessoa')
            horario = dados.get('horario')
            status_acesso = dados.get('status_acesso')

            if not all([id_cartao, nome_pessoa, horario, status_acesso]):
                return 'Dados incompletos', 400

            # Insert data into the database
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO registros_acesso (id_cartao, nome_pessoa, horario, status_acesso) VALUES (?, ?, ?, ?)",
                           (id_cartao, nome_pessoa, horario, status_acesso))
            conn.commit()
            conn.close()

            logging.info(f"Dados recebidos: {dados}")
            return 'Dados recebidos e inseridos no banco de dados com sucesso!', 200
        except Exception as e:
            logging.error(f"Erro ao processar os dados: {e}")
            return 'Erro ao processar os dados', 500
    else:
        return 'Método de requisição inválido', 405

# Route to return access records in JSON format


@app.route('/registros_acesso', methods=['GET'])
def obter_registros_acesso():
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM registros_acesso")
        registros = cursor.fetchall()
        conn.close()

        # Convert records into a list of dictionaries
        registros_json = []
        for registro in registros:
            registro_json = {
                'id': registro[0],
                'id_cartao': registro[1],
                'nome_pessoa': registro[2],
                'horario': registro[3],
                'status_acesso': registro[4]
            }
            registros_json.append(registro_json)

        return jsonify(registros_json), 200
    except Exception as e:
        logging.error(f"Erro ao obter registros: {e}")
        return 'Erro ao obter registros', 500


if __name__ == '__main__':
    # Create the table in the database if it doesn't exist yet
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS registros_acesso
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           id_cartao INTEGER,
                           nome_pessoa TEXT,
                           horario DATETIME,
                           status_acesso TEXT)''')
        conn.close()
        logging.info("Tabela 'registros_acesso' criada ou já existe.")
    except Exception as e:
        logging.error(f"Erro ao criar a tabela: {e}")

    # Start the Flask server
    app.run(host='54.233.158.31', port=5000)

