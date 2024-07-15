import sqlite3
from datetime import datetime

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('estudo.db')
cursor = conn.cursor()

# Criar a tabela de estudo
cursor.execute('''
    CREATE TABLE IF NOT EXISTS estudo (
        id INTEGER PRIMARY KEY,
        data TEXT,
        hora_inicio TEXT,
        hora_termino TEXT,
        atividade TEXT,
        foco INTEGER,
        comentarios TEXT
    )
''')

# Commit e fechar a conexão
conn.commit()
conn.close()