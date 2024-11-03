<?php
$pdo = new PDO('sqlite:supermercado.db');

$stmt = $pdo->query("SELECT * FROM Vendas");
$vendas = $stmt->fetchAll(PDO::FETCH_ASSOC);

echo "<h1>Relatório de Vendas</h1>";
echo "<table border='1'>";
echo "<tr><th>ID Venda</th><th>ID Cliente</th><th>Total</th><th>Data</th><th>Status</th></tr>";
foreach ($vendas as $venda) {
    echo "<tr>
            <td>{$venda['id_venda']}</td>
            <td>{$venda['id_cliente']}</td>
            <td>{$venda['total']}</td>
            <td>{$venda['data']}</td>
            <td>{$venda['status']}</td>
          </tr>";
}
echo "</table>";
?>