# RELATÓRIO DE AULA PRÁTICA: DESENVOLVIMENTO EM JAVASCRIPT

**Experimento:** Jogo de Jokenpô

**Disciplina:** Desenvolvimento em JavaScript

**Unidade:** U3_PROGRAMAÇÃO ORIENTADA A EVENTOS

**Aula:** A4_EVENTOS_EM_NÍVEL_DE_PÁGINA

---

## SUMÁRIO

1. [INTRODUÇÃO](#introdução)
2. [OBJETIVOS](#objetivos)
3. [SOLUÇÃO DIGITAL E FERRAMENTAS UTILIZADAS](#solução-digital-e-ferramentas-utilizadas)
4. [DESENVOLVIMENTO E PROCEDIMENTOS PRÁTICOS](#desenvolvimento-e-procedimentos-práticos)
4.1 [Estrutura do Projeto](#estrutura-do-projeto)
4.2 [Código HTML (`index.html`)](#código-html-(`index.html`))
4.3 [Estilização e Animações CSS (`style.css`)](#estilização-e-animações-css-(`style.css`))
4.4 [Lógica de Programação JavaScript (`script.js`)](#lógica-de-programação-javascript-(`script.js`))
5. [EVIDÊNCIAS DE EXECUÇÃO (PRINTS DO EXERCÍCIO)](#evidências-de-execução-(prints-do-exercício))
6. [AVALIANDO OS RESULTADOS (QUESTÃO TEÓRICA)](#avaliando-os-resultados-(questão-teórica))
7. [CONSIDERAÇÕES FINAIS E RESULTADOS DE APRENDIZAGEM](#considerações-finais-e-resultados-de-aprendizagem)
8. [REFERÊNCIAS BIBLIOGRÁFICAS](#referências-bibliográficas)

---

## 1. INTRODUÇÃO

Neste relatório, apresento a documentação técnica da construção de uma aplicação web interativa: o jogo de **Jokenpô** (Pedra, Papel e Tesoura). Durante a atividade prática, trabalhei com a integração de três tecnologias fundamentais do desenvolvimento Front-End: HTML5, que utilizei para estruturar semanticamente a página; CSS3, que apliquei na estilização e nas animações visuais; e JavaScript (ES6), que empreguei na lógica do jogo, no tratamento dos eventos do usuário e na manipulação dinâmica do DOM (Document Object Model).

---

## 2. OBJETIVOS

Com esta atividade, busquei desenvolver uma interface interativa baseada em eventos HTML5 e animações CSS3, aplicar a lógica condicional e a manipulação do DOM em JavaScript para gerenciar partidas contra o computador, criar uma experiência dinâmica, responsiva e fluida e compreender o fluxo de captura dos eventos do usuário, como os cliques nos botões, além da geração de escolhas aleatórias pelo sistema.

---

## 3. SOLUÇÃO DIGITAL E FERRAMENTAS UTILIZADAS

Para desenvolver o experimento, utilizei o **Visual Studio Code (VS Code)** como editor de código-fonte para escrever, organizar e depurar os arquivos do projeto. Também utilizei um navegador web, como o **Google Chrome** ou o **Mozilla Firefox**, para executar a aplicação e testar sua interface gráfica. As tecnologias empregadas foram **HTML5, CSS3 e JavaScript ES6**, responsáveis, respectivamente, pela estrutura, apresentação visual e comportamento interativo da página.

---

## 4. DESENVOLVIMENTO E PROCEDIMENTOS PRÁTICOS

### 4.1 Estrutura do Projeto

Organizei o projeto em três arquivos principais para separar as responsabilidades. No arquivo `index.html`, coloquei os elementos estruturais da página, incluindo os botões de escolha, as áreas do placar e a arena de comparação. No arquivo `style.css`, defini a apresentação visual, a responsividade e os efeitos de animação exibidos quando uma opção é selecionada. Por fim, no arquivo `script.js`, implementei as regras do jogo — pedra vence tesoura, papel vence pedra e tesoura vence papel —, o sorteio da jogada do computador e o controle da pontuação.

---

### 4.2 Código HTML (`index.html`)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jogo de Jokenpô - Aula Prática</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>Jokenpô</h1>
        <p class="instrucao">Escolha sua jogada para enfrentar o computador:</p>

        <!-- Botões de Escolha do Usuário -->
        <div class="opcoes">
            <button class="btn-opcao" id="pedra" onclick="jogar('pedra')">
                <span class="icone">🪨</span>
                <span>Pedra</span>
            </button>
            <button class="btn-opcao" id="papel" onclick="jogar('papel')">
                <span class="icone">📄</span>
                <span>Papel</span>
            </button>
            <button class="btn-opcao" id="tesoura" onclick="jogar('tesoura')">
                <span class="icone">✂️</span>
                <span>Tesoura</span>
            </button>
        </div>

        <!-- Arena de Comparação -->
        <div class="arena">
            <div class="card-jogada">
                <h3>Você</h3>
                <div class="escolha-box" id="escolha-usuario">❓</div>
            </div>
            <div class="vs">VS</div>
            <div class="card-jogada">
                <h3>Computador</h3>
                <div class="escolha-box" id="escolha-computador">❓</div>
            </div>
        </div>

        <!-- Exibição do Resultado -->
        <div class="resultado-box">
            <h2 id="mensagem-resultado">Faça sua escolha!</h2>
        </div>

        <!-- Placar e Reinício -->
        <div class="placar">
            <p>Vitórias: <span id="vitorias">0</span> | Derrotas: <span id="derrotas">0</span> | Empates: <span id="empates">0</span></p>
        </div>

        <button class="btn-reiniciar" onclick="reiniciarJogo()">Reiniciar Placar</button>
    </div>

    <script src="script.js"></script>
</body>
</html>

```

---

### 4.3 Estilização e Animações CSS (`style.css`)

```css
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
    background-color: #1e1e2e;
    color: #cdd6f4;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
}

.container {
    background: #181825;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    text-align: center;
    max-width: 500px;
    width: 100%;
}

h1 {
    color: #89b4fa;
    margin-bottom: 8px;
}

.instrucao {
    font-size: 0.95rem;
    color: #a6adc8;
    margin-bottom: 25px;
}

.opcoes {
    display: flex;
    justify-content: space-between;
    gap: 15px;
    margin-bottom: 30px;
}

.btn-opcao {
    flex: 1;
    background: #313244;
    border: 2px solid transparent;
    border-radius: 12px;
    padding: 15px 10px;
    color: #cdd6f4;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
}

.btn-opcao .icone {
    font-size: 2rem;
}

.btn-opcao:hover {
    background: #45475a;
    border-color: #89b4fa;
    transform: translateY(-4px);
}

.btn-opcao:active {
    transform: translateY(0);
}

.arena {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin-bottom: 25px;
}

.card-jogada h3 {
    font-size: 0.9rem;
    color: #a6adc8;
    margin-bottom: 8px;
}

.escolha-box {
    width: 70px;
    height: 70px;
    background: #313244;
    border-radius: 50%;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 2rem;
    margin: 0 auto;
    transition: transform 0.3s ease;
}

.vs {
    font-weight: bold;
    color: #f38ba8;
    font-size: 1.2rem;
}

.animar {
    animation: pop 0.4s ease-in-out;
}

@keyframes pop {
    0% { transform: scale(0.8); }
    50% { transform: scale(1.2); }
    100% { transform: scale(1); }
}

.resultado-box {
    min-height: 40px;
    margin-bottom: 20px;
}

#mensagem-resultado {
    font-size: 1.3rem;
    font-weight: 600;
}

.vitoria { color: #a6e3a1; }
.derrota { color: #f38ba8; }
.empate  { color: #f9e2af; }

.placar {
    font-size: 0.9rem;
    color: #bac2de;
    margin-bottom: 20px;
    padding-top: 15px;
    border-top: 1px solid #313244;
}

.btn-reiniciar {
    background: transparent;
    border: 1px solid #f38ba8;
    color: #f38ba8;
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.85rem;
    transition: background 0.2s;
}

.btn-reiniciar:hover {
    background: rgba(243, 139, 168, 0.1);
}

```

---

### 4.4 Lógica de Programação JavaScript (`script.js`)

```javascript
const elEscolhaUsuario = document.getElementById('escolha-usuario');
const elEscolhaComputador = document.getElementById('escolha-computador');
const elMensagemResultado = document.getElementById('mensagem-resultado');
const elVitorias = document.getElementById('vitorias');
const elDerrotas = document.getElementById('derrotas');
const elEmpates = document.getElementById('empates');

const icones = {
    pedra: '🪨',
    papel: '📄',
    tesoura: '✂️'
};

let vitorias = 0;
let derrotas = 0;
let empates = 0;

function jogar(escolhaUsuario) {
    const opcoes = ['pedra', 'papel', 'tesoura'];
    const escolhaComputador = opcoes[Math.floor(Math.random() * 3)];

    elEscolhaUsuario.textContent = icones[escolhaUsuario];
    elEscolhaComputador.textContent = icones[escolhaComputador];

    elEscolhaUsuario.classList.remove('animar');
    elEscolhaComputador.classList.remove('animar');
    void elEscolhaUsuario.offsetWidth; 
    elEscolhaUsuario.classList.add('animar');
    elEscolhaComputador.classList.add('animar');

    const resultado = calcularResultado(escolhaUsuario, escolhaComputador);
    atualizarPlacarEResultado(resultado);
}

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

function atualizarPlacarEResultado(resultado) {
    elMensagemResultado.className = '';

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

```

---

## 5. EVIDÊNCIAS DE EXECUÇÃO (PRINTS DO EXERCÍCIO)

Neste espaço, inserirei as capturas de tela que comprovam a execução do projeto no navegador. A primeira captura deverá apresentar a tela inicial do jogo, com os botões de ação e a arena em seu estado inicial (`❓`). A segunda deverá mostrar uma partida concluída, incluindo a escolha do jogador, a jogada sorteada pelo computador, a mensagem de resultado com o estilo visual correspondente e a atualização do placar.

---

## 6. AVALIANDO OS RESULTADOS (QUESTÃO TEÓRICA)

**Cenário/Questão:**

*Durante o desenvolvimento da página web “Gerador de Tabuada Interativo”, que utiliza JavaScript para calcular e exibir os resultados com base no número informado pelo usuário, por que é importante compreender e aplicar estruturas de repetição, como o laço “for”, em sistemas interativos como o proposto nesta atividade?*

**Resposta:**

Compreendi que as estruturas de repetição, como o laço `for`, são importantes em sistemas interativos porque permitem automatizar tarefas repetitivas sem duplicar manualmente as instruções no código. No cenário do *Gerador de Tabuada* apresentado na questão, eu utilizaria o `for` para percorrer uma sequência de valores e calcular as multiplicações, por exemplo, de 1 a 10, exibindo os resultados de forma organizada. Essa estrutura também pode ser aplicada ao jogo de *Jokenpô* para percorrer coleções de elementos do DOM, como os botões de escolha, ou vetores de opções e registros de partidas. Dessa forma, consigo escrever um código mais organizado, facilitar sua manutenção e reduzir a repetição de instruções.

---

## 7. CONSIDERAÇÕES FINAIS E RESULTADOS DE APRENDIZAGEM

Ao realizar esta atividade prática, consolidei meus conhecimentos sobre programação orientada a eventos no ambiente Web. Aprendi a estruturar e integrar páginas utilizando HTML, CSS e JavaScript, pratiquei a manipulação dinâmica de elementos por meio do DOM e o tratamento de eventos com `onclick`. Também desenvolvi feedback visual dinâmico, utilizando animações CSS acionadas pelo JavaScript. Essa experiência contribuiu para ampliar minha compreensão sobre a interação entre a estrutura, o estilo e o comportamento de uma aplicação web.

---

## 8. REFERÊNCIAS BIBLIOGRÁFICAS

* MDN WEB DOCS. **JavaScript: Guias e Referência**. Mozilla Developer Network. Disponível em: [https://developer.mozilla.org/pt-BR/docs/Web/JavaScript](https://developer.mozilla.org/pt-BR/docs/Web/JavaScript). Acesso em: 2026.
* W3SCHOOLS. **JavaScript DOM Events**. Disponível em: [https://www.w3schools.com/js/js_events.asp](https://www.w3schools.com/js/js_events.asp). Acesso em: 2026.
* FLANAGAN, David. **JavaScript: O Guia Definitivo**. 7. ed. Porto Alegre: Bookman, 2021.