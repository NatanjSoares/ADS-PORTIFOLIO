// js/index.js
const formulario = document.getElementById('formulario');

function calcularIMC(peso, altura) {
    const resultado = Number(peso) / (Number(altura) * Number(altura));
    return resultado.toFixed(2);
}

function classificarIMC(imc) {
    if (imc < 18.5) return 'Abaixo do peso';
    if (imc < 25) return 'Peso normal';
    if (imc < 30) return 'Sobrepeso';
    if (imc < 35) return 'Obesidade grau I';
    if (imc < 40) return 'Obesidade grau II';
    return 'Obesidade grau III';
}

formulario.addEventListener('submit', function (event) {
    event.preventDefault(); // evita recarregar a página

    const peso = document.getElementById('peso').value;
    const altura = document.getElementById('altura').value;

    const valorIMC = calcularIMC(peso, altura);

    document.getElementById('resultado-imc').innerText = valorIMC;
    document.getElementById('classificacao-imc').innerText = classificarIMC(valorIMC);
});