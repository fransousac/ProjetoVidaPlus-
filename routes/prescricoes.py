from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import sqlite3

bp_prescricoes = Blueprint('prescricoes', __name__, url_prefix='/prescricoes')

def conectar_db():
    return sqlite3.connect('banco.db')

@bp_prescricoes.route('/', methods=['GET'])
@jwt_required()
def listar_prescricoes():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT pr.id, pa.nome, pf.nome, pr.receita, pr.data
        FROM prescricoes pr
        JOIN pacientes pa ON pr.id_paciente = pa.id
        JOIN profissionais pf ON pr.id_profissional = pf.id
    ''')
    prescricoes = cursor.fetchall()
    conn.close()
    lista = []
    for pr in prescricoes:
        lista.append({
            'id': pr[0],
            'paciente': pr[1],
            'profissional': pr[2],
            'receita': pr[3],
            'data': pr[4]
        })
    return jsonify(lista)

@bp_prescricoes.route('/', methods=['POST'])
@jwt_required()
def criar_prescricao():
    dados = request.get_json()
    id_paciente = dados.get('id_paciente')
    id_profissional = dados.get('id_profissional')
    receita = dados.get('receita')
    data = dados.get('data')
    if not (id_paciente and id_profissional and receita and data):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO prescricoes (id_paciente, id_profissional, receita, data)
        VALUES (?, ?, ?, ?)
    ''', (id_paciente, id_profissional, receita, data))
    conn.commit()
    id_novo = cursor.lastrowid
    conn.close()
    return jsonify({'id': id_novo, 'id_paciente': id_paciente, 'id_profissional': id_profissional, 'receita': receita, 'data': data}), 201

@bp_prescricoes.route('/<int:id>', methods=['PUT'])
@jwt_required()
def editar_prescricao(id):
    dados = request.get_json()
    id_paciente = dados.get('id_paciente')
    id_profissional = dados.get('id_profissional')
    receita = dados.get('receita')
    data = dados.get('data')
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM prescricoes WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'erro': 'Prescrição não encontrada'}), 404
    cursor.execute('''
        UPDATE prescricoes
        SET id_paciente=?, id_profissional=?, receita=?, data=?
        WHERE id=?
    ''', (id_paciente, id_profissional, receita, data, id))
    conn.commit()
    conn.close()
    return jsonify({'id': id, 'id_paciente': id_paciente, 'id_profissional': id_profissional, 'receita': receita, 'data': data})

@bp_prescricoes.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_prescricao(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM prescricoes WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'erro': 'Prescrição não encontrada'}), 404
    cursor.execute("DELETE FROM prescricoes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Prescrição excluída com sucesso'}), 200
