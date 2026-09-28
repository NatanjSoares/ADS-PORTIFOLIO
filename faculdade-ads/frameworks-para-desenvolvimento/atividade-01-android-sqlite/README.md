# Atividade 01 — Cadastro de produtos no Android (SQLite)

Aplicativo Android nativo para cadastrar e listar produtos, com os dados salvos em um banco **SQLite** local.

## O que tem aqui

- `MainActivity.kt` — tela (layout em XML), validações e lista de produtos. Regras: nome com no mínimo 3 caracteres e preço maior que zero; mensagens de erro/sucesso via `Toast`.
- `ProdutoDbHelper.java` — `SQLiteOpenHelper` com o banco `produtos.db` e a tabela `produtos` (`id`, `nome`, `preco`). Métodos `inserirproduto` e `listarProdutos`.
- `Produto.java` — modelo com `id`, `nome` e `preco`.
- `relatorio-atividade-01.pdf` — relatório da atividade (arquitetura, desafios e respostas do roteiro).

## Tecnologias

Kotlin · Java · Android SDK · SQLite · Gradle

## Como executar

Abra esta pasta no **Android Studio**, aguarde a sincronização do Gradle e execute em um emulador ou dispositivo.
