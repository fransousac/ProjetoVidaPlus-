from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required  # Importa o decorador
import sqlite3

bp_pacientes = Blueprint('pacientes', __name__, url_prefix='/pacientes')

def conectar_db():
    return sqlite3.connect('banco.db')

@bp_pacientes.route('/', methods=['GET'])
@jwt_required()  # Protegendo a rota
def listar_pacientes():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, idade, telefone FROM pacientes")
    pacientes = cursor.fetchall()
    conn.close()
    lista = [{'id': p[0], 'nome': p[1], 'idade': p[2], 'telefone': p[3]} for p in pacientes]
    return jsonify(lista)

@bp_pacientes.route('/', methods=['POST'])
@jwt_required()
def criar_paciente():
    dados = request.get_json()
    nome = dados.get('nome')
    idade = dados.get('idade')
    telefone = dados.get('telefone')
    if not nome:
        return jsonify({'erro': 'Nome é obrigatório'}), 400
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pacientes (nome, idade, telefone) VALUES (?, ?, ?)", (nome, idade, telefone))
    conn.commit()
    id_novo = cursor.lastrowid
    conn.close()
    return jsonify({'id': id_novo, 'nome': nome, 'idade': idade, 'telefone': telefone}), 201

@bp_pacientes.route('/<int:id>', methods=['PUT'])
@jwt_required()
def editar_paciente(id):
    dados = request.get_json()
    nome = dados.get('nome')
    idade = dados.get('idade')
    telefone = dados.get('telefone')
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM pacientes WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'erro': 'Paciente não encontrado'}), 404
    cursor.execute("UPDATE pacientes SET nome=?, idade=?, telefone=? WHERE id=?", (nome, idade, telefone, id))
    conn.commit()
    conn.close()
    return jsonify({'id': id, 'nome': nome, 'idade': idade, 'telefone': telefone})

@bp_pacientes.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_paciente(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM pacientes WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'erro': 'Paciente não encontrado'}), 404
    cursor.execute("DELETE FROM pacientes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Paciente excluído com sucesso'}), 200
