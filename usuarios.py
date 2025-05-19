import sqlite3

conn = sqlite3.connect('banco.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

print("Tabela 'usuarios' criada com sucesso.")
