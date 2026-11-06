const formulario = document.getElementById("formTabuada");
const campoNumero = document.getElementById("numeroInput");
const resultadoDiv = document.getElementById("resultado");

formulario.addEventListener("submit", function (evento) {
    evento.preventDefault();

    const numero = Number(campoNumero.value);

    resultadoDiv.innerHTML = "";

    // Validação do número informado
    if (!Number.isInteger(numero) || numero < 1 || numero > 10) {
        resultadoDiv.innerHTML =
            '<p class="erro">Insira um número inteiro entre 1 e 10.</p>';
        return;
    }

    // Criação da lista de resultados
    const lista = document.createElement("ul");

    // Estrutura de repetição FOR
    for (let i = 1; i <= 10; i++) {
        const resultado = numero * i;

        const item = document.createElement("li");

        item.textContent = `${numero} x ${i} = ${resultado}`;

        lista.appendChild(item);
    }

    // Exibição na página através do DOM
    const titulo = document.createElement("strong");

    titulo.textContent = `Tabuada do ${numero}:`;

    resultadoDiv.appendChild(titulo);
    resultadoDiv.appendChild(lista);
});

