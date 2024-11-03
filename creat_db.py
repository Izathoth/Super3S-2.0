import sqlite3

def criar_banco():
    conn = sqlite3.connect('supermercado.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Clientes (
                        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        cpf TEXT NOT NULL,
                        endereco TEXT NOT NULL,
                        email TEXT NOT NULL,
                        telefone TEXT NOT NULL
                      );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Produtos (
                        id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        quantidade_estoque INTEGER NOT NULL,
                        preco REAL NOT NULL
                      );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Vendas (
                        id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_cliente INTEGER,
                        total REAL NOT NULL,
                        forma_pagamento TEXT NOT NULL,
                        status TEXT NOT NULL,
                        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (id_cliente) REFERENCES Clientes (id_cliente)
                      );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ItensVenda (
                        id_item INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_venda INTEGER,
                        id_produto INTEGER,
                        quantidade INTEGER NOT NULL,
                        preco REAL NOT NULL,
                        FOREIGN KEY (id_venda) REFERENCES Vendas (id_venda),
                        FOREIGN KEY (id_produto) REFERENCES Produtos (id_produto)
                      );''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    criar_banco()
    print("Banco de dados criado com sucesso!")