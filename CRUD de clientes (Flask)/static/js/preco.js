document.addEventListener("DOMContentLoaded", () => {
  const custo = document.getElementById("custo");
  const mult = document.getElementById("multiplicador");
  const preco = document.getElementById("preco");

  // sai sem erro se a página não tiver esses campos
  if (!custo || !mult || !preco) return;

  function calcular() {
    const c = parseFloat(custo.value);
    const m = parseFloat(mult.value);

    if (c > 0 && m > 0) {
      preco.value = (c * m).toFixed(2);
      preco.readOnly = true;
    } else {
      preco.readOnly = false;
    }
  }

  custo.addEventListener("input", calcular);
  mult.addEventListener("change", calcular);
  calcular();
});