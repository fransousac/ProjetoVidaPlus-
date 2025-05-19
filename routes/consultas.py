from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import sqlite3

bp_consultas = Blueprint('consultas', __name__, url_prefix='/consultas')

def conectar_db():
    return sqlite3.connect('banco.db')

@bp_consultas.route('/', methods=['GET'])
@jwt_required()
def listar_consultas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.id, pa.nome, pf.nome, c.data, c.status
        FROM consultas c
        JOIN pacientes pa ON c.id_paciente = pa.id
        JOIN profissionais pf ON c.id_profissional = pf.id
    ''')
    consultas = cursor.fetchall()
    conn.close()
    lista = []
    for c in consultas:
        lista.append({
            'id': c[0],
            'paciente': c[1],
            'profissional': c[2],
            'data': c[3],
            'status': c[4]
        })
    return jsonify(lista)

@bp_consultas.route('/debug_raw', methods=['GET'])
def listar_consultas_raw():
    """Lista consultas sem JOIN para ajudar a diagnosticar dados."""
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM consultas")
    consultas = cursor.fetchall()
    conn.close()
    lista = []
    for c in consultas:
        lista.append({
            'id': c[0],
            'id_paciente': c[1],
            'id_profissional': c[2],
            'data': c[3],
            'status': c[4]
        })
    return jsonify(lista)

@bp_consultas.route('/', methods=['POST'])
@jwt_required()
def criar_consulta():
    dados = request.get_json()
    id_paciente = dados.get('id_paciente')
    id_profissional = dados.get('id_profissional')
    data = dados.get('data')
    status = dados.get('status', 'agendada')

    if not (id_paciente and id_profissional and data):
        return jsonify({'erro': 'id_paciente, id_profissional e data são obrigatórios'}), 400

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO consultas (id_paciente, id_profissional, data, status)
        VALUES (?, ?, ?, ?)
    ''', (id_paciente, id_profissional, data, status))
    conn.commit()
    id_novo = cursor.lastrowid
    conn.close()

    return jsonify({
        'id': id_novo,
        'id_paciente': id_paciente,
        'id_profissional': id_profissional,
        'data': data,
        'status': status
    }), 201

@bp_consultas.route('/<int:id>', methods=['PUT'])
@jwt_required()
def editar_consulta(id):
    dados = request.get_json()
    id_paciente = dados.get('id_paciente')
    id_profissional = dados.get('id_profissional')
    data = dados.get('data')
    status = dados.get('status', 'agendada')

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM consultas WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'erro': 'Consulta não encontrada'}), 404

    cursor.execute('''
        UPDATE consultas
        SET id_paciente=?, id_profissional=?, data=?, status=?
        WHERE id=?
    ''', (id_paciente, id_profissional, data, status, id))
    conn.commit()
    conn.close()

    return jsonify({
        'id': id,
        'id_paciente': id_paciente,
        'id_profissional': id_profissional,
        'data': data,
        'status': status
    })

@bp_consultas.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def excluir_consulta(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM consultas WHERE id = ?", (id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'erro': 'Consulta não encontrada'}), 404

    cursor.execute("DELETE FROM consultas WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return jsonify({'mensagem': 'Consulta excluída com sucesso'}), 200
