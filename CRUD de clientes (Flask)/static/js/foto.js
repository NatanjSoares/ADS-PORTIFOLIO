document.addEventListener("DOMContentLoaded", () => {
  const campo = document.getElementById("foto");
  if (!campo) return;

  const LIMITE = 2 * 1024 * 1024; // 2 MB
  const TIPOS = ["image/jpeg", "image/png", "image/webp"];
  const aviso = document.getElementById("foto-aviso");
  const previa = document.getElementById("foto-previa");
  let urlAtual = null;

  function mostrarAviso(texto) {
    if (aviso) aviso.textContent = texto;
  }

  campo.addEventListener("change", () => {
    mostrarAviso("");

    if (previa) previa.hidden = true;
    if (urlAtual) {
      URL.revokeObjectURL(urlAtual);
      urlAtual = null;
    }

    const arquivo = campo.files[0];
    if (!arquivo) return;

    if (arquivo.type && !TIPOS.includes(arquivo.type)) {
      mostrarAviso("Formato inválido. Use JPG, PNG ou WEBP.");
      campo.value = "";
      return;
    }

    if (arquivo.size > LIMITE) {
      mostrarAviso("A foto deve ter no máximo 2 MB.");
      campo.value = "";
      return;
    }

    if (previa) {
      urlAtual = URL.createObjectURL(arquivo);
      previa.src = urlAtual;
      previa.hidden = false;
    }
  });
});