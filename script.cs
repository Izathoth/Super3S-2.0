using Microsoft.AspNetCore.Mvc;
using Microsoft.Data.Sqlite;

namespace Supermercado.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class VendasController : ControllerBase
    {
        private string connectionString = "Data Source=supermercado.db";

        [HttpPost]
        public IActionResult RegistrarVenda([FromBody] Venda venda)
        {
            using (var connection = new SqliteConnection(connectionString))
            {
                connection.Open();
                var transaction = connection.BeginTransaction();

                var total = venda.Produtos.Sum(p => p.Preco * p.Quantidade);
                var command = new SqliteCommand("INSERT INTO Vendas (id_cliente, total, forma_pagamento, status) VALUES (@id_cliente, @total, @forma_pagamento, 'completa')", connection);
                command.Parameters.AddWithValue("@id_cliente", venda.IdCliente);
                command.Parameters.AddWithValue("@total", total);
                command.Parameters.AddWithValue("@forma_pagamento", venda.FormaPagamento);
                command.ExecuteNonQuery();

                foreach (var produto in venda.Produtos)
                {
                    command = new SqliteCommand("INSERT INTO ItensVenda (id_venda, id_produto, quantidade, preco) VALUES (last_insert_rowid(), @id_produto, @quantidade, @preco)", connection);
                    command.Parameters.AddWithValue("@id_produto", produto.IdProduto);
                    command.Parameters.AddWithValue("@quantidade", produto.Quantidade);
                    command.Parameters.AddWithValue("@preco", produto.Preco);
                    command.ExecuteNonQuery();

                    command = new SqliteCommand("UPDATE Produtos SET quantidade_estoque = quantidade_estoque - @quantidade WHERE id_produto = @id_produto", connection);
                    command.Parameters.AddWithValue("@quantidade", produto.Quantidade);
                    command.Parameters.AddWithValue("@id_produto", produto.IdProduto);
                    command.ExecuteNonQuery();
                }

                transaction.Commit();
            }

            return Ok(new { message = "Venda registrada com sucesso!" });
        }
    }

    public class Venda
    {
        public int IdCliente { get; set; }
        public string FormaPagamento { get; set; }
        public List<Produto> Produtos { get; set; }
    }

    public class Produto
    {
        public int IdProduto { get; set; }
        public int Quantidade { get; set; }
        public decimal Preco { get; set; }
    }
}