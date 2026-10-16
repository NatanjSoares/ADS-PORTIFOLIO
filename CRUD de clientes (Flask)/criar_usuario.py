import getpass
from contextlib import closing

from werkzeug.security import generate_password_hash

import produtos
import usuarios

usuarios.inicializar_usuarios()  # garante que a tabela existe

usuario = input("Usuário: ").strip()
senha = getpass.getpass("Senha: ")
confirmacao = getpass.getpass("Repita a senha: ")

if not usuario or not senha:
    raise SystemExit("Usuário e senha são obrigatórios.")
if senha != confirmacao:
    raise SystemExit("As senhas não conferem.")

with closing(produtos._conectar()) as conexao, conexao:
    conexao.execute(
        """
        INSERT INTO usuarios (usuario, senha_hash) VALUES (?, ?)
        ON CONFLICT(usuario) DO UPDATE SET senha_hash = excluded.senha_hash
        """,
        (usuario, generate_password_hash(senha)),
    )

print("Usuário salvo.")
