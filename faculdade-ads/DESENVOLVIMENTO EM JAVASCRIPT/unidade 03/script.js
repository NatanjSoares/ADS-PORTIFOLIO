// Mapeamento dos elementos do DOM
const elEscolhaUsuario = document.getElementById('escolha-usuario');
const elEscolhaComputador = document.getElementById('escolha-computador');
const elMensagemResultado = document.getElementById('mensagem-resultado');
const elVitorias = document.getElementById('vitorias');
const elDerrotas = document.getElementById('derrotas');
const elEmpates = document.getElementById('empates');

// Icones para exibição
const icones = {
    pedra: '🪨',
    papel: '📄',
    tesoura: '✂️'
};

// Controle de Placar
let vitorias = 0;
let derrotas = 0;
let empates = 0;

// Função principal disparada pelo clique nas opções
function jogar(escolhaUsuario) {
    const opcoes = ['pedra', 'papel', 'tesoura'];
    const escolhaComputador = opcoes[Math.floor(Math.random() * 3)];

    // Atualiza a exibição das escolhas na tela
    elEscolhaUsuario.textContent = icones[escolhaUsuario];
    elEscolhaComputador.textContent = icones[escolhaComputador];

    // Adiciona efeito visual de animação
    elEscolhaUsuario.classList.remove('animar');
    elEscolhaComputador.classList.remove('animar');
    void elEscolhaUsuario.offsetWidth; // Força reflow para reiniciar animação CSS
    elEscolhaUsuario.classList.add('animar');
    elEscolhaComputador.classList.add('animar');

    // Determina o vencedor
    const resultado = calcularResultado(escolhaUsuario, escolhaComputador);
    atualizarPlacarEResultado(resultado, escolhaUsuario, escolhaComputador);
}

// Lógica das regras do Jokenpô
function calcularResultado(usuario, computador) {
    if (usuario === computador) {
        return 'empate';
    }

    if (
        (usuario === 'pedra' && computador === 'tesoura') ||
        (usuario === 'papel' && computador === 'pedra') ||
        (usuario === 'tesoura' && computador === 'papel')
    ) {
        return 'vitoria';
    }

    return 'derrota';
}

// Atualiza os textos e contadores na interface
function atualizarPlacarEResultado(resultado) {
    elMensagemResultado.className = ''; // Reseta classes de cores

    if (resultado === 'vitoria') {
        vitorias++;
        elVitorias.textContent = vitorias;
        elMensagemResultado.textContent = 'Você Venceu! 🎉';
        elMensagemResultado.classList.add('vitoria');
    } else if (resultado === 'derrota') {
        derrotas++;
        elDerrotas.textContent = derrotas;
        elMensagemResultado.textContent = 'Você Perdeu! 😢';
        elMensagemResultado.classList.add('derrota');
    } else {
        empates++;
        elEmpates.textContent = empates;
        elMensagemResultado.textContent = 'Empate! ⚖️';
        elMensagemResultado.classList.add('empate');
    }
}

// Reinicia o placar e a arena
function reiniciarJogo() {
    vitorias = 0;
    derrotas = 0;
    empates = 0;

    elVitorias.textContent = '0';
    elDerrotas.textContent = '0';
    elEmpates.textContent = '0';

    elEscolhaUsuario.textContent = '❓';
    elEscolhaComputador.textContent = '❓';
    elMensagemResultado.textContent = 'Faça sua escolha!';
    elMensagemResultado.className = '';
}
