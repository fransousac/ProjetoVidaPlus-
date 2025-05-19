
import sqlite3

def conectar_db():
    conn = sqlite3.connect('banco.db')
    return conn

def criar_tabelas():
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            telefone TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profissionais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            especialidade TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescricoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER NOT NULL,
            id_profissional INTEGER NOT NULL,
            receita TEXT NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (id_paciente) REFERENCES pacientes(id),
            FOREIGN KEY (id_profissional) REFERENCES profissionais(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER NOT NULL,
            id_profissional INTEGER NOT NULL,
            data TEXT NOT NULL,
            status TEXT DEFAULT 'agendada',
            FOREIGN KEY (id_paciente) REFERENCES pacientes(id),
            FOREIGN KEY (id_profissional) REFERENCES profissionais(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
