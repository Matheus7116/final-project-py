CREATE DATABASE IF NOT EXISTS supermercado;
USE supermercado;

CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    marca VARCHAR(100) NOT NULL,
    nome VARCHAR(100) NOT NULL,
    preco DECIMAL(10,2) NOT NULL,
    qtde_estoque INT NOT NULL
);

CREATE TABLE IF NOT EXISTS funcionarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    salario DECIMAL(10,2) NOT NULL,
    telefone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    endereco VARCHAR(200),
    email VARCHAR(100),
    telefone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_venda DATETIME NOT NULL,
    id_funcionario INT,
    id_cliente INT,
    id_produto INT,
    qtde_comprada INT NOT NULL,
    valor_total DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id),
    FOREIGN KEY (id_produto) REFERENCES produtos(id)
);