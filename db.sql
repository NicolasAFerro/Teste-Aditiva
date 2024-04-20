CREATE TABLE Clientes (
    id INT PRIMARY KEY,
    Nome VARCHAR(100),
    Idade INT
); 

CREATE TABLE Simulacoes (
    id INT PRIMARY KEY,
    cliente_id INT,
    Descricao VARCHAR(255),
    Capital FLOAT,
    Premio_mensal FLOAT,
    Premio_anual FLOAT,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);