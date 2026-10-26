import getpass
from contextlib import closing

from flask import Flask
from werkzeug.security import generate_password_hash

from adonai.config import caminho_do_banco
from adonai.dados import banco, usuarios

app = Flask(__name__)
app.config["DB_PATH"] = caminho_do_banco()

with app.app_context():
    banco.inicializar_banco()
    usuarios.inicializar_usuarios()  # garante que a tabela existe

    usuario = input("Usuário: ").strip()
    senha = getpass.getpass("Senha: ")
    confirmacao = getpass.getpass("Repita a senha: ")

    if not usuario or not senha:
        raise SystemExit("Usuário e senha são obrigatórios.")
    if senha != confirmacao:
        raise SystemExit("As senhas não conferem.")

    with closing(banco.conectar()) as conexao, conexao:
        conexao.execute(
            """
            INSERT INTO usuarios (usuario, senha_hash) VALUES (?, ?)
            ON CONFLICT(usuario) DO UPDATE SET senha_hash = excluded.senha_hash
            """,
            (usuario, generate_password_hash(senha)),
        )

    print("Usuário salvo.")