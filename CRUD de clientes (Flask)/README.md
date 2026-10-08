# ADONAI — Sistema de Gestão de Produtos

CRUD de produtos para uma marca de prata e semijoias, desenvolvido em Flask com identidade visual própria (verde esmeralda, dourado e marfim).

![Home](docs/home.png)

## Funcionalidades

- Cadastro, edição e exclusão de produtos (nome, categoria, preço, estoque e descrição)
- Listagem com busca por nome
- Validação dos campos no servidor, com mensagens de erro e sucesso
- Interface responsiva, com CSS modular
- 10 testes automatizados (banco e rotas)
| Lista de produtos | Cadastro |
|---|---|
| ![Produtos](docs/produtos.png) | ![Cadastro](docs/cadastro.png) |

## Tecnologias

- Python 3.13 e Flask
- SQLite
- HTML5 e CSS3 (variáveis, grid e flexbox)
- Docker e Docker Compose

## Estrutura

```
CRUD de clientes (Flask)/
├── app.py              # rotas e validação
├── produtos.py         # acesso ao banco de dados
├── templates/          # base, home, listar e form
├── static/
│   ├── css/            # CSS dividido em módulos
│   └── img/            # hero e favicons
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Como executar

### Com Docker

1. Crie o arquivo `.env` a partir do exemplo e preencha a chave:
```
   python -c "import secrets; print(secrets.token_hex(32))"
```
```
   SECRET_KEY=cole-a-chave-aqui
```
2. Suba a aplicação:
```
   docker compose up --build
```
3. Acesse http://localhost:5001

O banco fica na pasta `data/`, então os dados permanecem entre execuções.

### Sem Docker

```
pip install -r requirements.txt
$env:SECRET_KEY="sua-chave"     # PowerShell
python app.py
```
Acesse http://127.0.0.1:5000

### Testes

```
pip install pytest
python -m pytest -v
```
Os testes usam um banco temporário e não alteram os seus dados.


## Aprendizados


- Separação entre rotas (`app.py`) e acesso a dados (`produtos.py`)
- Herança de templates com Jinja2
- CSS modular com variáveis para a identidade visual
- Containerização com Docker e persistência do banco em volume
- Variáveis de ambiente para dados sensíveis

## Próximos passos

- Proteção CSRF com Flask-WTF
- Preço armazenado em centavos
- Login de usuário e upload de foto do produto
- Deploy online

## Autor

**Natan** — estudante de Análise e Desenvolvimento de Sistemas.
[GitHub](https://github.com/NatanjSoares)