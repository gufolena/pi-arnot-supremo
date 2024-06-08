from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import logging
import os

app = Flask(__name__)
CORS(app)

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Setup logging
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

# Info log configuration
info_handler = logging.FileHandler("logs/info.log", mode='a')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(log_formatter)

# Error log configuration
error_handler = logging.FileHandler("logs/error.log", mode='a')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(log_formatter)

# Console log configuration
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(log_formatter)

# Adding handlers to the root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)  # Capture all levels of logs
root_logger.addHandler(info_handler)
root_logger.addHandler(error_handler)
root_logger.addHandler(console_handler)

# Function to connect to the database


def conectar_bd():
    return sqlite3.connect('database.db')

# Function to create a table if it doesn't exist


def criar_tabela():
    try:
        with conectar_bd() as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS registros_acesso
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               id_cartao INTEGER,
                               nome_pessoa TEXT,
                               horario DATETIME,
                               status_acesso TEXT)''')
            logging.info("Tabela 'registros_acesso' criada ou já existe.")
    except sqlite3.Error as e:
        logging.error(f"Erro ao criar a tabela: {e}")

# Route to receive data from the device


@app.route('/receber_dados', methods=['POST'])
def receber_dados():
    if request.method == 'POST':
        try:
            dados = request.json  # Assumes that the data is sent as JSON
            id_cartao = dados.get('id_cartao')
            nome_pessoa = dados.get('nome_pessoa')
            horario = dados.get('horario')
            status_acesso = dados.get('status_acesso')

            if not all([id_cartao, nome_pessoa, horario, status_acesso]):
                logging.warning("Dados incompletos recebidos.")
                return 'Dados incompletos', 400

            # Insert data into the database
            with conectar_bd() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO registros_acesso (id_cartao, nome_pessoa, horario, status_acesso) VALUES (?, ?, ?, ?)",
                               (id_cartao, nome_pessoa, horario, status_acesso))
                conn.commit()

            logging.info(f"Dados recebidos: {dados}")
            return 'Dados recebidos e inseridos no banco de dados com sucesso!', 200
        except sqlite3.Error as e:
            logging.error(f"Erro ao processar os dados no banco de dados: {e}")
            return 'Erro ao processar os dados no banco de dados', 500
        except Exception as e:
            logging.error(f"Erro ao processar os dados: {e}")
            return 'Erro ao processar os dados', 500
    else:
        logging.warning("Método de requisição inválido usado.")
        return 'Método de requisição inválido', 405

# Route to return access records in JSON format


@app.route('/registros_acesso', methods=['GET'])
def obter_registros_acesso():
    try:
        with conectar_bd() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM registros_acesso")
            registros = cursor.fetchall()

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

        logging.info("Registros de acesso obtidos com sucesso.")
        return jsonify(registros_json), 200
    except sqlite3.Error as e:
        logging.error(f"Erro ao obter registros do banco de dados: {e}")
        return 'Erro ao obter registros do banco de dados', 500
    except Exception as e:
        logging.error(f"Erro ao obter registros: {e}")
        return 'Erro ao obter registros', 500


if __name__ == '__main__':
    # Create the table in the database if it doesn't exist yet
    criar_tabela()

    # Start the Flask server
    app.run(host='54.233.158.31', port=5000)
