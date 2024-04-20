import pdfplumber
import re  
import pyodbc
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

"""cliente1 = Cliente("João", 30, [
    Cobertura("Seguro de vida", 100000, 50.0, 600.0),
    Cobertura("Seguro de carro", 20000, 100.0, 1200.0)
]) """
#da para colocar uma entrada se quiser com o caminho para ficar dinamico se todos os arquivos forem iguais
#caminho PDF estava dando errado pois não estava colocando o nome do arquivo
caminhopdf =r"C://Users//Nicolas//Documents//Teste-Aditiva//pdfTeste.pdf"#o erro estava dando aqui, tem que colocar um raw de cru na frente

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
            padrao = r'(.+?)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)'#finalmente
            cobertura = re.findall(padrao, text)
            #cobertura= re.findall(r'(\w+(?:\s\w+)*)\s+([\d.,]+)\s+([\d.,]+)\s+([\d.,]+)', text)
            for match in cobertura:
                descricao: str
                capital: float
                premio_mensal: float
                premio_anual: float
                descricao, capital_str, premio_mensal_str, premio_anual_str = match
                capital_str = capital_str.replace('.', '').replace(',', '.')
                capital = float(capital_str)
                premio_mensal_str = premio_mensal_str.replace(',', '.')
                premio_mensal = float(premio_mensal_str) 
                premio_anual_str = premio_anual_str.replace('.', '').replace(',', '.')
                premio_anual = float(premio_anual_str)
                cobertura = Cobertura(descricao.strip(), capital, premio_mensal, premio_anual)
                coberturas.append(cobertura)

            # objeto Cliente e retorna
            cliente: Cliente = Cliente(nome_cliente, idade_cliente, coberturas)
            return cliente 
    
cliente: Cliente = converterPdf(caminhopdf)


print("Nome:", cliente.nome)
print("Idade:", cliente.idade)
print("Coberturas:")
for cobertura in cliente.coberturas:
    print("  Descrição:", cobertura.descricao)
    print("  Capital:", cobertura.capital)
    print("  Prêmio Mensal:", cobertura.premio_mensal)
    print("  Prêmio Anual:", cobertura.premio_anual)
    print()

