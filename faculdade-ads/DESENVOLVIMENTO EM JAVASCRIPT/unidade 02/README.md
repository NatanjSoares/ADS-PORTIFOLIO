# Animação Interativa com Canvas HTML5

Projeto desenvolvido como atividade prática da disciplina
**Desenvolvimento em JavaScript**, da Universidade Anhanguera, com foco
na manipulação gráfica e na criação de animações utilizando HTML5 Canvas
e JavaScript.

## Objetivo

Desenvolver uma aplicação web capaz de desenhar e animar objetos
geométricos no elemento `<canvas>`, atualizar suas propriedades
dinamicamente e permitir interação com o usuário por meio do clique do
mouse.

## Tecnologias utilizadas

-   HTML5
-   CSS3
-   JavaScript
-   Canvas API
-   `requestAnimationFrame()`

## Estrutura do projeto

``` text
animacao-canvas/
├── index.html
├── style.css
├── script.js
└── README.md
```

## Funcionalidades

-   Desenho de esferas no Canvas.
-   Movimento contínuo dos objetos.
-   Atualização das posições nos eixos X e Y.
-   Detecção de colisões com as bordas do Canvas.
-   Alteração aleatória das cores das esferas ao clicar na área de
    animação.
-   Utilização de estruturas de repetição para percorrer e atualizar os
    objetos.

## Como executar

1.  Baixe ou clone este projeto para o computador.
2.  Abra a pasta do projeto no Visual Studio Code ou em outro editor de
    código.
3.  Verifique se os arquivos `index.html`, `style.css` e `script.js`
    estão na mesma pasta.
4.  Abra o arquivo `index.html` em um navegador, como Google Chrome,
    Microsoft Edge ou Mozilla Firefox.
5.  Observe as esferas em movimento e clique dentro do Canvas para
    alterar suas cores.

Não é necessário instalar dependências ou utilizar um servidor para
executar esta versão simples do projeto.

## Organização do código

### `index.html`

Contém a estrutura da página, o elemento `<canvas>` utilizado para a
animação e as referências aos arquivos CSS e JavaScript.

### `style.css`

Define a apresentação visual da página, incluindo alinhamento, cores,
espaçamentos e aparência do Canvas.

### `script.js`

Contém a lógica da aplicação. O código define a classe `Esfera`,
inicializa os objetos, atualiza suas posições, verifica colisões com as
bordas e controla a interação de clique. O método
`requestAnimationFrame()` é utilizado para manter o ciclo de animação.

## Conceitos praticados

-   Manipulação do DOM.
-   Declaração de variáveis e constantes.
-   Classes e objetos em JavaScript.
-   Arrays e métodos de iteração.
-   Estruturas de repetição.
-   Funções e eventos.
-   Geração de valores aleatórios.
-   Desenho bidimensional com Canvas.
-   Animação com `requestAnimationFrame()`.

## Evidências da execução

As evidências podem ser adicionadas a esta seção após a execução do
projeto. Recomenda-se incluir capturas de tela do código no editor e da
aplicação no navegador, mostrando as esferas em movimento antes e depois
do clique para alteração das cores.

## Contexto acadêmico

**Instituição:** Universidade Anhanguera\
**Curso:** Análise e Desenvolvimento de Sistemas\
**Disciplina:** Desenvolvimento em JavaScript\
**Atividade:** Unidade 2 -- Animação com Canvas\
**Aluno:** Natan de Jesus Soares\
**Local:** Mogi das Cruzes -- SP\
**Ano:** 2026

## Referências

-   MDN WEB DOCS. [Canvas API -- Web
    APIs](https://developer.mozilla.org/pt-BR/docs/Web/API/Canvas_API).
    Mozilla Developer Network.
-   MDN WEB DOCS.
    [Window.requestAnimationFrame()](https://developer.mozilla.org/pt-BR/docs/Web/API/Window/requestAnimationFrame).
    Mozilla Developer Network.
-   FLANAGAN, David. *JavaScript: O Guia Definitivo*. 6. ed. Porto
    Alegre: Bookman, 2013.
