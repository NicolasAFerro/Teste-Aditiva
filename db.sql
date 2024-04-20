

CREATE TABLE Clientes (
    id INT PRIMARY KEY IDENTITY,
    Nome VARCHAR(100),
    Idade INT
); 

CREATE TABLE Simulacoes (
    id INT PRIMARY KEY IDENTITY,
    cliente_id INT,
    Descricao VARCHAR(255),
    Capital FLOAT,
    Premio_mensal FLOAT,
    Premio_anual FLOAT,
    FOREIGN KEY (Cliente_id) REFERENCES Clientes(id)
); 

SELECT * FROM Clientes 
SELECT * FROM Simulacoes
DELETE FROM Clientes 
DELETE FROM Simulacoes