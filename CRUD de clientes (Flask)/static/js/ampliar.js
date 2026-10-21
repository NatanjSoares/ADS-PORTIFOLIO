document.addEventListener("DOMContentLoaded", () => {
  const dialogo = document.getElementById("foto-dialogo");
  const grande = document.getElementById("foto-grande");
  const fechar = document.getElementById("foto-fechar");

  if (!dialogo || !grande || typeof dialogo.showModal !== "function") return;

  function abrir(miniatura) {
    grande.src = miniatura.dataset.grande;
    grande.alt = miniatura.alt;
    dialogo.showModal();
  }

  document.querySelectorAll(".foto-ampliavel").forEach((miniatura) => {
    miniatura.addEventListener("click", () => abrir(miniatura));
    miniatura.addEventListener("keydown", (evento) => {
      if (evento.key === "Enter" || evento.key === " ") {
        evento.preventDefault();
        abrir(miniatura);
      }
    });
  });

  if (fechar) fechar.addEventListener("click", () => dialogo.close());

  // clique no fundo escuro (fora da foto) também fecha
  dialogo.addEventListener("click", (evento) => {
    if (evento.target === dialogo) dialogo.close();
  });

  dialogo.addEventListener("close", () => grande.removeAttribute("src"));
});