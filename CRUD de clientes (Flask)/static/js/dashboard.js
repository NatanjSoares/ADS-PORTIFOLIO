document.addEventListener("DOMContentLoaded", () => {
  const el = document.getElementById("dados-dashboard");
  if (!el || typeof Chart === "undefined") return;

  const d = JSON.parse(el.textContent);

  const verde = "#00382F";
  const dourado = "#C59F6D";
  const douradoEscuro = "#94744D";
  const paleta = [verde, dourado, douradoEscuro, "#143427", "#F3E0C7", "#212A2D"];

  Chart.defaults.font.family = "Montserrat, system-ui, sans-serif";
  
    Chart.defaults.maintainAspectRatio = false;

  const reais = (v) => "R$ " + Number(v).toFixed(2);

  // 1. Estoque por produto
  new Chart(document.getElementById("grafico-estoque"), {
    type: "bar",
    data: {
      labels: d.nomes,
      datasets: [{ label: "Unidades", data: d.estoque, backgroundColor: verde }],
    },
    options: {
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } },
    },
  });

  // 2. Custo x preço de venda (só produtos com custo)
  const canvasPreco = document.getElementById("grafico-preco");
  if (d.custos.length === 0) {
    canvasPreco.replaceWith("Cadastre produtos com custo para ver este gráfico.");
  } else {
    new Chart(canvasPreco, {
      type: "bar",
      data: {
        labels: d.custo_nomes,
        datasets: [
          { label: "Custo + embalagem", data: d.custos, backgroundColor: douradoEscuro },
          { label: "Preço de venda", data: d.precos, backgroundColor: verde },
        ],
      },
      options: {
        scales: { y: { beginAtZero: true, ticks: { callback: reais } } },
        plugins: {
          tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${reais(c.raw)}` } },
        },
      },
    });
  }

  // 3. Produtos por categoria
  new Chart(document.getElementById("grafico-categoria"), {
    type: "doughnut",
    data: {
      labels: d.categorias,
      datasets: [{ data: d.qtd_categorias, backgroundColor: paleta }],
    },
  });
});