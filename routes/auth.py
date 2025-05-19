from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')

def conectar_db():
    return sqlite3.connect('banco.db')

# ROTA DE CADASTRO
@bp_auth.route('/signup', methods=['POST'])
def signup():
    try:
        dados = request.get_json()
        email = dados.get('email')
        senha = dados.get('senha')

        if not email or not senha:
            return jsonify({'erro': 'Email e senha são obrigatórios'}), 400

        senha_hash = generate_password_hash(senha)

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (email, senha) VALUES (?, ?)", (email, senha_hash))
        conn.commit()

        return jsonify({'mensagem': 'Usuário criado com sucesso'}), 201

    except sqlite3.IntegrityError:
        return jsonify({'erro': 'Email já cadastrado'}), 400

    except Exception as e:
        return jsonify({'erro': f'Erro no cadastro: {str(e)}'}), 500

    finally:
        conn.close()

# ROTA DE LOGIN
@bp_auth.route('/login', methods=['POST'])
def login():
    try:
        dados = request.get_json()
        email = dados.get('email')
        senha = dados.get('senha')

        if not email or not senha:
            return jsonify({'erro': 'Email e senha são obrigatórios'}), 400

        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, senha FROM usuarios WHERE email = ?", (email,))
        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario[1], senha):
            token = create_access_token(identity=usuario[0])
            return jsonify({'token': token})

        return jsonify({'erro': 'Credenciais inválidas'}), 401

    except Exception as e:
        return jsonify({'erro': f'Erro no login: {str(e)}'}), 500

    finally:
        conn.close()
