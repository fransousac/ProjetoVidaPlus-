from database import conectar_db

def criar_paciente(nome, idade, telefone):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO pacientes (nome, idade, telefone) VALUES (?, ?, ?)', (nome, idade, telefone))
    conn.commit()
    conn.close()

def listar_pacientes():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes')
    pacientes = cursor.fetchall()
    conn.close()
    return pacientes

def obter_paciente(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pacientes WHERE id = ?', (id,))
    paciente = cursor.fetchone()
    conn.close()
    return paciente

def atualizar_paciente(id, nome, idade, telefone):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE pacientes SET nome = ?, idade = ?, telefone = ? WHERE id = ?', (nome, idade, telefone, id))
    conn.commit()
    conn.close()

def excluir_paciente(id):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pacientes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
