# Atividade 01 — Calculadora com testes unitários (JUnit 5)

Classe `Calculadora` em Java com as quatro operações básicas e uma suíte de testes unitários escrita com **JUnit 5**.

## O que tem aqui

- `src/main/java/Calculadora.java` — `somar`, `subtrair`, `multiplicar` e `dividir` (a divisão por zero lança `ArithmeticException`).
- `src/test/java/CalculadoraTest.java` — 6 testes unitários e 1 teste parametrizado (`@ParameterizedTest` com `@CsvSource`, 4 casos), cobrindo:
  - resultado de cada operação;
  - soma com número negativo;
  - exceção ao dividir por zero (`assertThrows`).
- `pom.xml` — projeto Maven com a dependência `junit-jupiter` 5.12.2.

## Tecnologias

Java · JUnit 5 · Maven · IntelliJ IDEA

## Como executar os testes

Pela IDE (IntelliJ: botão de executar em `CalculadoraTest`) ou pelo terminal, na pasta do projeto:

```bash
mvn test
```
