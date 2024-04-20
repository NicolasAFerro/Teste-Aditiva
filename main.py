import pdfplumber
import re 
from typing import List

class Cobertura:
    def __init__(self, descricao: str, capital: float, premio_mensal: float, premio_anual: float):
        self.descricao: str = descricao
        self.capital: float = capital
        self.premio_mensal: float = premio_mensal
        self.premio_anual: float = premio_anual

class Cliente:
    def __init__(self, nome: str, idade: int, coberturas: list):
        self.nome: str = nome
        self.idade: int = idade
        self.coberturas: List[Cobertura] = coberturas

cliente1 = Cliente("João", 30, [
    Cobertura("Seguro de vida", 100000, 50.0, 600.0),
    Cobertura("Seguro de carro", 20000, 100.0, 1200.0)
]) 

#caminho PDF 
caminhopdf: str =r"C:\\Users\\Nicolas\\Documents\\Teste-Aditiva"#o erro estava dando aqui, tem que colocar um raw de cru na frente

def converterPdf(caminhopdf: str) -> Cliente:
    with pdfplumber.open(caminhopdf) as pdf:
        page = pdf.pages[0]  # Extrai apenas a primeira página
        text: str = page.extract_text() 

# padrão "Cliente: Nome do Cliente, Idade"
        cliente_match = re.search(r'Cliente: (\w+\s\w+), (\d+)', text)
        if cliente_match:
            nome_cliente: str = cliente_match.group(1)
            idade_cliente: int = int(cliente_match.group(2)) 


            coberturas: List[Cobertura] = []
            cobertura_matches = re.findall(r'Cobertura: (.+?) - Capital: (\d+), Prêmio Mensal: (\d+\.?\d*), Prêmio Anual: (\d+\.?\d*)', text)
            for match in cobertura_matches:
                descricao: str
                capital: float
                premio_mensal: float
                premio_anual: float
                descricao, capital_str, premio_mensal_str, premio_anual_str = match
                capital = float(capital_str)
                premio_mensal = float(premio_mensal_str)
                premio_anual = float(premio_anual_str)
                cobertura = Cobertura(descricao.strip(), capital, premio_mensal, premio_anual)
                coberturas.append(cobertura)

            # objeto Cliente e retorna
            cliente: Cliente = Cliente(nome_cliente, idade_cliente, coberturas)
            return cliente 
    
#cliente: Cliente = converterPdf(caminhopdf)


print("Nome:", cliente1.nome)
print("Idade:", cliente1.idade)
print("Coberturas:")
for cobertura in cliente1.coberturas:
    print("  Descrição:", cobertura.descricao)
    print("  Capital:", cobertura.capital)
    print("  Prêmio Mensal:", cobertura.premio_mensal)
    print("  Prêmio Anual:", cobertura.premio_anual)
    print()

