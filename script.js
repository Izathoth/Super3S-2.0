document.getElementById('formVenda').onsubmit = async function (event) {
    event.preventDefault();
    const clienteId = document.getElementById('id_cliente').value;
    const formaPagamento = document.getElementById('forma_pagamento').value;

    const produtos = Array.from(document.querySelectorAll('#produtos input')).reduce((acc, input, index) => {
        if (index % 3 === 0) {
            acc.push({ id_produto: input.value });
        } else if (index % 3 === 1) {
            acc[acc.length - 1].quantidade = input.value;
        } else {
            acc[acc.length - 1].preco = input.value;
        }
        return acc;
    }, []);

    const response = await fetch('/vendas', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id_cliente: clienteId, forma_pagamento: formaPagamento, produtos }),
    });
    const data = await response.json();
    alert(data.message);
};