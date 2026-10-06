# CRUD de Produtos (Flask)

Aplicação web para cadastrar, listar, editar, buscar e excluir produtos.
Projeto do meu portfólio de Análise e Desenvolvimento de Sistemas.

## Funcionalidades

- Cadastro de produtos (nome, categoria, preço, estoque e descrição)
- Listagem com busca por nome
- Edição e exclusão de produtos
- Validação dos campos no servidor, com mensagens de erro e sucesso

## Tecnologias

- Python 3.13
- Flask
- SQLite
- HTML5 e CSS3 (modularizado)
- Docker e Docker Compose

## Estrutura

```
CRUD de clientes (Flask)/
├── app.py              # rotas e validação
├── produtos.py         # acesso ao banco de dados
├── templates/          # base, home, listar e form
├── static/css/         # CSS dividido em módulos
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Como executar

### Com Docker

1. Copie `.env.example` para `.env` e preencha a `SECRET_KEY`:
```
   python -c "import secrets; print(secrets.token_hex(32))"
```
2. Suba a aplicação:
```
   docker compose up --build
```
3. Acesse http://localhost:5001

O banco fica salvo na pasta `data/`, então os dados permanecem entre execuções.

### Sem Docker

```
pip install -r requirements.txt
$env:SECRET_KEY="sua-chave"     # PowerShell
python app.py
```

## Próximos passos

- Proteção CSRF com Flask-WTF
- Preço armazenado em centavos
- Testes automatizados

## Autor

Natan, estudante de ADS na Universidade Anhanguera.