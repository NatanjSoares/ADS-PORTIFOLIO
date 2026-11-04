console.log("Calculo de IMC ");

function calcularIMC(peso, altura) {
    let resultado = Number(peso) / (Number(altura) * Number(altura));
    
    return resultado.toFixed(2);
}

console.log(calcularIMC('70', '1.75'));