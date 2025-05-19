from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import sqlite3

bp_profissionais = Blueprint('profissionais', __name__, url_prefix='/profissionais')

def conectar_db():
    return sqlite3.connect('banco.db')

@bp_profissionais.route('/', methods=['GET'])
@jwt_required()
def listar_profissionais():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, especialidade FROM profissionais")
    profissionais = cursor.fetchall()
    conn.close()
    lista = [{'id': p[0], 'nome': p[1], 'especialidade': p[2]} for p in profissionais]
    return jsonify(lista)

@bp_profissionais.route('/', methods=['POST'])
@jwt_required()
def criar_profissional():
    dados = request.get_json()
    nome = dados.get('nome')
    especialidade = dados.get('especialidade')
    if not nome:
        return jsonify({'erro': 'Nome é obrigatório'}), 400
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO profissionais (nome, especialidade) VALUES (?, ?)", (nome, especialidade))
    conn.commit()
    id_novo = cursor.lastrowid
    conn.close()
    return jsonify({'id': id_novo, 'nome': nome, 'especialidade': especialidade}), 201

@bp_profissionais.route('/<int:id>', methods=['PUT'])
@jwt_required()
def editar_profissional(id):
    dados = request.get_json()
    nome = dados.get('nome')
    especialidade = dados.get('especialidade')
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM profissionais WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'erro': 'Profissional não encontrado'}), 404
    cursor.execute("UPDATE profissionais SET nome=?, especialidade=? WHERE id=?", (nome, especialidade, id))
    conn.commit()
    conn.close()
    return jsonify({'id': id, 'nome': nome, 'especialidade': especialidade})

@bp_profissionais.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_profissional(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM profissionais WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'erro': 'Profissional não encontrado'}), 404
    cursor.execute("DELETE FROM profissionais WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Profissional excluído com sucesso'}), 200
