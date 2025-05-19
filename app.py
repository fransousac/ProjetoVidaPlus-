from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import sqlite3
from datetime import timedelta

from routes.pacientes import bp_pacientes
from routes.profissionais import bp_profissionais
from routes.consultas import bp_consultas
from routes.prescricoes import bp_prescricoes
from routes.auth import bp_auth  # <-- ADICIONAR ISSO

app = Flask(__name__)

# Configuração do segredo do JWT (troque essa chave para algo seguro)
app.config['JWT_SECRET_KEY'] = 'supersecreto123'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=6)
jwt = JWTManager(app)

def conectar_db():
    return sqlite3.connect('banco.db')

@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    username = dados.get('username')
    senha = dados.get('senha')

    if not username or not senha:
        return jsonify({"erro": "Username e senha são obrigatórios"}), 400

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT senha FROM usuarios WHERE username = ?", (username,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario and usuario[0] == senha:
        token = create_access_token(identity=username)
        return jsonify({"token": token})
    else:
        return jsonify({"erro": "Usuário ou senha incorretos"}), 401

# Registrando os blueprints das rotas
app.register_blueprint(bp_pacientes)
app.register_blueprint(bp_profissionais)
app.register_blueprint(bp_consultas)
app.register_blueprint(bp_prescricoes)
app.register_blueprint(bp_auth)  # <-- ADICIONAR ISSO

if __name__ == '__main__':
    app.run(debug=True)
