from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def db_connection():
    conn = sqlite3.connect('supermercado.db')
    return conn

@app.route('/clientes', methods=['POST'])
def adicionar_cliente():
    conn = db_connection()
    cursor = conn.cursor()
    new_cliente = request.json
    cursor.execute("INSERT INTO Clientes (nome, cpf, endereco, email, telefone) VALUES (?, ?, ?, ?, ?)",
                   (new_cliente['nome'], new_cliente['cpf'], new_cliente['endereco'], new_cliente['email'], new_cliente['telefone']))
    conn.commit()
    return jsonify({"message": "Cliente adicionado com sucesso!"}), 201

@app.route('/vendas', methods=['POST'])
def registrar_venda():
    conn = db_connection()
    cursor = conn.cursor()
    venda_data = request.json
    total = sum(item['preco'] * item['quantidade'] for item in venda_data['produtos'])
    
    cursor.execute("INSERT INTO Vendas (id_cliente, total, forma_pagamento, status) VALUES (?, ?, ?, 'completa')",
                   (venda_data['id_cliente'], total, venda_data['forma_pagamento']))
    venda_id = cursor.lastrowid
    
    for produto in venda_data['produtos']:
        cursor.execute("INSERT INTO ItensVenda (id_venda, id_produto, quantidade, preco) VALUES (?, ?, ?, ?)",
                       (venda_id, produto['id_produto'], produto['quantidade'], produto['preco']))
        cursor.execute("UPDATE Produtos SET quantidade_estoque = quantidade_estoque - ? WHERE id_produto = ?",
                       (produto['quantidade'], produto['id_produto']))
    conn.commit()
    return jsonify({"message": "Venda registrada com sucesso!"}), 201

if __name__ == '__main__':
    app.run(debug=True)