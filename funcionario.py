class Funcionario:
    def __init__ (self, id, nome, salario):
        self.id = id    
        self.nome = nome
        self.salario = salario
    def situacao(self, limite=3000):
        return "Acima da Média" if self.salario >= limite else "Abaixo da Média"