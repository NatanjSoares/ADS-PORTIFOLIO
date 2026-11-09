# Qualidade e Automação de Testes

## 1. Sobre o projeto

Este projeto foi desenvolvido como atividade prática da disciplina **Qualidade e Automação de Testes**, do curso de Análise e Desenvolvimento de Sistemas (ADS), da Universidade Anhanguera.

A atividade consiste na implementação de uma função em Python para comparar dois números e identificar o maior valor, utilizando estruturas condicionais e testes automatizados para validar seu funcionamento.

## 2. Objetivos

- Aplicar conceitos de qualidade de software.
- Desenvolver uma função utilizando Python.
- Implementar testes de caixa branca.
- Criar cenários de testes unitários.
- Automatizar a execução dos testes.
- Verificar os resultados obtidos em relação aos resultados esperados.

## 3. Tecnologias e ferramentas

| Tecnologia | Utilização |
|---|---|
| Python 3.13.14 | Linguagem de programação |
| Visual Studio Code | Ambiente de desenvolvimento |
| unittest | Framework de testes automatizados |
| PowerShell | Terminal para execução dos comandos |

## 4. Estrutura do projeto

```text
qualidade-automacao-testes/
│
├── main.py
├── testes.py
├── README.md
└── __pycache__/
```

### Descrição dos arquivos

- **main.py:** contém a função `maximo()`, responsável pela comparação dos valores.
- **testes.py:** contém os três cenários de testes automatizados utilizando unittest.
- **README.md:** documentação do projeto.

## 5. Implementação

A função `maximo()` utiliza estruturas condicionais para identificar três situações:

1. Primeiro número maior que o segundo.
2. Segundo número maior que o primeiro.
3. Dois números com valores iguais.

As estruturas condicionais utilizadas são `if`, `elif` e `else`.

## 6. Cenários de testes

Foram implementados três casos de teste:

| Identificação | Valores de entrada | Resultado esperado |
|---|---|---|
| CT01 | 10 e 20 | O número 20 é o maior. |
| CT02 | 390 e 380 | O número 390 é o maior. |
| CT03 | 50 e 50 | Os dois números são iguais. |

## 7. Execução do projeto

Para executar a aplicação pelo terminal integrado do Visual Studio Code, utilize:

```powershell
python main.py
```

Para executar os testes automatizados:

```powershell
python -m unittest -v
```

## 8. Resultados obtidos

Após a implementação e execução dos testes, obtive os seguintes resultados:

- Total de testes: 3.
- Testes aprovados: 3.
- Testes reprovados: 0.
- Taxa de aprovação: 100%.

Resultado apresentado pelo terminal:

```text
Ran 3 tests in 0.003s

OK
```

## 9. Conceitos aplicados

**Teste de caixa branca:** verificação dos caminhos condicionais da função implementada.

**Teste unitário:** validação individual do comportamento da função `maximo()`.

**Teste automatizado:** utilização do unittest para executar os cenários e comparar os resultados esperados com os obtidos.

## 10. Considerações finais

A realização desta atividade permitiu aplicar conceitos fundamentais de qualidade e automação de testes de software.

Durante o desenvolvimento, implementei uma função em Python e desenvolvi três cenários de testes para verificar diferentes possibilidades de comparação numérica.

A utilização do framework unittest possibilitou automatizar a validação do código e confirmar que todos os cenários apresentaram os resultados esperados.

Concluí que a aplicação de testes automatizados contribui para aumentar a confiabilidade, identificar possíveis falhas e melhorar a qualidade do software.

---

**Instituição:** Universidade Anhanguera  
**Curso:** Análise e Desenvolvimento de Sistemas  
**Disciplina:** Qualidade e Automação de Testes  
**Aluno:** Natan de Jesus Soares  
**Local:** Mogi das Cruzes – SP  
**Ano:** 2026