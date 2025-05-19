import os
from database import criar_tabelas, conectar_db

# Apaga o arquivo banco.db se existir
if os.path.exists('banco.db'):
    os.remove('banco.db')
    print("Arquivo banco.db apagado.")

# Cria as tabelas do banco
criar_tabelas()
print("Tabelas criadas.")
