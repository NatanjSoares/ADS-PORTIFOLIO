# Cadastro de clientes (terminal)

Dois scripts em Python que exercitam entrada de dados, validação, listas e dicionários.

## Arquivos

- `main.py` — cadastra um cliente e valida cada campo:
  - nome entre 5 e 35 caracteres;
  - idade numérica entre 1 e 120;
  - e-mail contendo `@` e `.`;
  - cidade com até 50 caracteres;
  - estado (UF) com 2 letras;
  - telefone numérico com 10 ou 11 dígitos.
- `menu.py` — menu interativo que guarda os clientes em uma lista de dicionários:
  1. cadastrar cliente (nome, idade, e-mail e cidade);
  2. listar clientes e mostrar o total;
  3. sair;
  4. buscar cliente por nome (ignora maiúsculas/minúsculas e aceita parte do nome).

  Depois de cada operação o programa pergunta se você deseja continuar.

Os dados do `menu.py` ficam apenas em memória: ao encerrar o programa, a lista é perdida.

## Tecnologias

Python 3

## Como executar

```bash
python main.py
python menu.py
```
