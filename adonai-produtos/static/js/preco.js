document.addEventListener("DOMContentLoaded", () => {
  const custo = document.getElementById("custo");
  const embalagem = document.getElementById("embalagem");
  const mult = document.getElementById("multiplicador");
  const preco = document.getElementById("preco");

  if (!custo || !mult || !preco) return;

  function emCentavos(campo) {
    const valor = campo ? parseFloat(campo.value) : 0;
    return valor > 0 ? Math.round(valor * 100) : 0;
  }

  function calcular() {
    const custoCentavos = emCentavos(custo);
    const base = custoCentavos + emCentavos(embalagem);
    const m = parseFloat(mult.value);

    if (custoCentavos > 0 && m > 0) {
      const m100 = Math.round(m * 100);
      const precoCentavos = Math.floor((base * m100 + 50) / 100);
      preco.value = (precoCentavos / 100).toFixed(2);
      preco.readOnly = true;
    } else {
      preco.readOnly = false;
    }
  }

  [custo, embalagem].forEach((campo) => {
    if (campo) campo.addEventListener("input", calcular);
  });
  mult.addEventListener("change", calcular);
  calcular();
});