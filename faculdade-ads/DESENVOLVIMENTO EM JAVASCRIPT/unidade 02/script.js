// Configuração Inicial do Canvas
const canvas = document.getElementById('meuCanvas');
const ctx = canvas.getContext('2d');

// Classe para representação das Esferas (Objetos Animados)
class Esfera {
    constructor(x, y, raio, dx, dy, cor) {
        this.x = x;
        this.y = y;
        this.raio = raio;
        this.dx = dx; // Velocidade no eixo X
        this.dy = dy; // Velocidade no eixo Y
        this.cor = cor;
    }

    // Desenha o objeto no canvas
    desenhar() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.raio, 0, Math.PI * 2, false);
        ctx.fillStyle = this.cor;
        ctx.fill();
        ctx.closePath();
    }

    // Atualiza a posição e trata colisões com as bordas
    atualizar() {
        // Colisão com as bordas laterais (esquerda/direita)
        if (this.x + this.raio > canvas.width || this.x - this.raio < 0) {
            this.dx = -this.dx;
        }

        // Colisão com as bordas superiores/inferiores
        if (this.y + this.raio > canvas.height || this.y - this.raio < 0) {
            this.dy = -this.dy;
        }

        this.x += this.dx;
        this.y += this.dy;

        this.desenhar();
    }

    // Altera a cor do objeto para um valor aleatório
    mudarCor() {
        const cores = ['#FF5733', '#33FF57', '#3357FF', '#F39C12', '#9B59B6', '#1ABC9C', '#E74C3C'];
        this.cor = cores[Math.floor(Math.random() * cores.length)];
    }
}

// Inicialização do array de objetos
const esferas = [];
const quantidadeEsferas = 15;

function inicializar() {
    esferas.length = 0;
    for (let i = 0; i < quantidadeEsferas; i++) {
        const raio = Math.random() * 15 + 10;
        const x = Math.random() * (canvas.width - raio * 2) + raio;
        const y = Math.random() * (canvas.height - raio * 2) + raio;
        const dx = (Math.random() - 0.5) * 4;
        const dy = (Math.random() - 0.5) * 4;
        const cor = '#38bdf8';

        esferas.push(new Esfera(x, y, raio, dx, dy, cor));
    }
}

// Loop de Animação Principal
function animar() {
    requestAnimationFrame(animar);
    
    // Limpa a tela a cada frame para evitar rastro
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Atualiza todos os objetos da tela
    for (let i = 0; i < esferas.length; i++) {
    esferas[i].atualizar();
}
}

// Interatividade: Clique para alterar as cores de todos os objetos
canvas.addEventListener('click', () => {
    esferas.forEach(esfera => esfera.mudarCor());
});

// Execução inicial
inicializar();
animar();
