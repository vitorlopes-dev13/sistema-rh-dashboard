import sqlite3

DB_NAME = "funcionario.db"

def conectar():
    return sqlite3.connect(DB_NAME)
def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute ("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            salario REAL NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()