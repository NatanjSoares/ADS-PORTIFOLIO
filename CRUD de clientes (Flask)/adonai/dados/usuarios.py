"""Acesso ao banco: tabela de usuários e verificação de login."""

import os
from contextlib import closing

from werkzeug.security import check_password_hash, generate_password_hash

from adonai.dados import banco

HASH_FALSO = generate_password_hash("senha-falsa")


def inicializar_usuarios():
    with closing(banco.conectar()) as conexao, conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL
            )
            """
        )

        usuario = os.environ.get("ADMIN_USER")
        senha = os.environ.get("ADMIN_PASSWORD")

        if usuario and senha:
            conexao.execute(
                """
                INSERT INTO usuarios (usuario, senha_hash) VALUES (?, ?)
                ON CONFLICT(usuario) DO UPDATE SET senha_hash = excluded.senha_hash
                """,
                (usuario, generate_password_hash(senha)),
            )


def verificar_login(usuario, senha):
    with closing(banco.conectar()) as conexao, conexao:
        linha = conexao.execute(
            "SELECT senha_hash FROM usuarios WHERE usuario = ?",
            (usuario,),
        ).fetchone()

    if linha is None:
        check_password_hash(HASH_FALSO, senha)
        return False

    return check_password_hash(linha["senha_hash"], senha)