class Cobertura:
    def __init__(self, descricao: str, capital: float, premio_mensal: float, premio_anual: float):
        self.descricao = descricao
        self.capital = capital
        self.premio_mensal = premio_mensal
        self.premio_anual = premio_anual

class Cliente:
    def __init__(self, nome: str, idade: int, coberturas: list):
        self.nome = nome
        self.idade = idade
        self.coberturas = coberturas

cliente1 = Cliente("João", 30, [
    Cobertura("Seguro de vida", 100000, 50.0, 600.0),
    Cobertura("Seguro de carro", 20000, 100.0, 1200.0)
]) 
"""
print("Nome:", cliente1.nome)
print("Idade:", cliente1.idade)
print("Coberturas:")
for cobertura in cliente1.coberturas:
    print("  Descrição:", cobertura.descricao)
    print("  Capital:", cobertura.capital)
    print("  Prêmio Mensal:", cobertura.premio_mensal)
    print("  Prêmio Anual:", cobertura.premio_anual)
    print()
    """