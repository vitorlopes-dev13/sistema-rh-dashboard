from database import conectar 
from funcionario import Funcionario

def cadastrar_funcionario(nome, salario):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO funcionarios (nome, salario) VALUES (?, ?)",
        (nome, salario)
    )

    conexao.commit()
    conexao.close()


def listar_funcionarios():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome, salario FROM funcionarios")
    dados = cursor.fetchall()
    conexao.close()

    return [Funcionario(id, nome, salario) for id, nome, salario in dados]


def calcular_media():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT AVG(salario) FROM funcionarios")
    resultado = cursor.fetchone()[0]

    conexao.close()
    return resultado if resultado else 0  

def atualizar_funcionario(id, nome, salario):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE funcionarios SET nome = ?, salario = ? WHERE id = ?",
        (nome, salario, id)
    )
    conexao.commit()
    conexao.close()

def deletar_funcionario(funcionario_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM funcionarios WHERE id = ?", (funcionario_id,))
    
    conexao.commit()
    conexao.close()


def resumo_dashboard():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM funcionarios")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(salario) FROM funcionarios")
    media = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM funcionarios WHERE salario >= 3000")
    acima = cursor.fetchone()[0]

    conexao.close()

    return total, (media if media else 0), acima  