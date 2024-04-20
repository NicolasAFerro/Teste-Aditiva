import pdfplumber #biblioteca que da o scrapping no pdf
import re  #expressoes regulares
import pyodbc #conexao com o banco pip install pyobdc
from typing import List

#conexao com o banco
try: 
    db_conexao= pyodbc.connect('Driver={SQL Server};'
    'Server=localhost\sqlexpress02;'
    'Database=testeAditiva;'
    'Trusted_Connection=yes;')
    print("\nbanco conectado")
except pyodbc.Error as erro: 
    print("Erro na conexão:", erro)

cursor = db_conexao.cursor()








#declaração das classes
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

#funcao para converter o pdf
try:
    def converterPdf(caminhopdf: str) -> Cliente:
        with pdfplumber.open(caminhopdf) as pdf:
            page = pdf.pages[0]  # Extrai apenas a primeira página
            text: str = page.extract_text() 


            cliente_match = re.search(r'Cliente: (\w+\s\w+), (\d+)', text)#expressao regular facil
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
                    capital_str = capital_str.replace('.', '').replace(',', '.')#cada campo esta com alguma coisa
                    capital = float(capital_str)
                    premio_mensal_str = premio_mensal_str.replace(',', '.')
                    premio_mensal = float(premio_mensal_str) 
                    premio_anual_str = premio_anual_str.replace('.', '').replace(',', '.')
                    premio_anual = float(premio_anual_str)
                    cobertura = Cobertura(descricao.strip(), capital, premio_mensal, premio_anual)
                    coberturas.append(cobertura)

                #   instancia do objeto Cliente 
                cliente: Cliente = Cliente(nome_cliente, idade_cliente, coberturas) 
                try: 
                    # Inserir cliente no banco de dados
                    cursor.execute("INSERT INTO clientes (Nome, Idade) VALUES (?, ?)", (cliente.nome, cliente.idade))
                    db_conexao.commit()

                    # Obter o ID do cliente inserido
                    cursor.execute("SELECT id FROM Clientes WHERE Nome = ?", (cliente.nome,))
                    cliente_id = cursor.fetchone()[0] 
                    print("ID do cliente recém-inserido:", cliente_id)

                    # Inserir coberturas no banco de dados
                    for cobertura in cliente.coberturas:
                        cursor.execute("INSERT INTO Simulacoes (cliente_id, Descricao, Capital, Premio_mensal, Premio_anual) VALUES (?, ?, ?, ?, ?)", (cliente_id, cobertura.descricao, cobertura.capital, cobertura.premio_mensal, cobertura.premio_anual))
                        db_conexao.commit() 

                    print("inserido no banco com sucesso")
                except pyodbc.Error as erro: 
                    print("\nerro ao inserir no banco", erro)

                

                return cliente 
                
except pyodbc.Error as erro: 
    print("\nerro na funcao de pdf")
        
cliente: Cliente = converterPdf(caminhopdf)## mds


print("Nome:", cliente.nome)
print("Idade:", cliente.idade)
print("Coberturas:")
for cobertura in cliente.coberturas:
    print("  Descrição:", cobertura.descricao)
    print("  Capital:", cobertura.capital)
    print("  Prêmio Mensal:", cobertura.premio_mensal)
    print("  Prêmio Anual:", cobertura.premio_anual)
    print()


#fechando a conexao com o banco    
try:
    db_conexao.close() 
    print("\nbanco fechado")
except pyodbc.Error as erro: 
    print("banco não fechou:", erro)
