"""Conexão e preparação do banco SQLite.

O caminho do arquivo vem de app.config["DB_PATH"]. Por isso estas funções
só rodam com um app ativo: dentro de uma requisição ou de
`with app.app_context():`.
"""

import sqlite3
from contextlib import closing
from pathlib import Path

from flask import current_app

SQL_TABELA_PRODUTOS = """
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        preco_centavos INTEGER NOT NULL,
        estoque INTEGER NOT NULL,
        descricao TEXT NOT NULL,
        custo_centavos INTEGER NOT NULL DEFAULT 0,
        multiplicador REAL NOT NULL DEFAULT 0,
        foto TEXT,
        embalagem_centavos INTEGER NOT NULL DEFAULT 0,
        frete_centavos INTEGER NOT NULL DEFAULT 0
    )
"""


def conectar():
    conexao = sqlite3.connect(current_app.config["DB_PATH"])
    conexao.row_factory = sqlite3.Row
    return conexao


def _migrar_para_centavos(conexao):
    """Converte a tabela antiga (reais em REAL) para centavos inteiros."""
    colunas = [c["name"] for c in conexao.execute("PRAGMA table_info(produtos)")]
    if "preco_centavos" in colunas:
        return

    custo = "CAST(ROUND(custo * 100) AS INTEGER)" if "custo" in colunas else "0"
    mult = "multiplicador" if "multiplicador" in colunas else "0"

    if not conexao.in_transaction:
        conexao.execute("BEGIN")

    conexao.execute("ALTER TABLE produtos RENAME TO produtos_antiga")
    conexao.execute(SQL_TABELA_PRODUTOS)
    conexao.execute(
        f"""
        INSERT INTO produtos
        (id, nome, categoria, preco_centavos, estoque, descricao,
         custo_centavos, multiplicador)
        SELECT id, nome, categoria, CAST(ROUND(preco * 100) AS INTEGER),
               estoque, descricao, {custo}, {mult}
        FROM produtos_antiga
        """
    )
    conexao.execute("DROP TABLE produtos_antiga")


def _adicionar_coluna_foto(conexao):
    """Bancos antigos ganham a coluna foto, sem perder dados."""
    colunas = [c["name"] for c in conexao.execute("PRAGMA table_info(produtos)")]
    if "foto" not in colunas:
        conexao.execute("ALTER TABLE produtos ADD COLUMN foto TEXT")


def _adicionar_colunas_embalagem_frete(conexao):
    """Bancos antigos ganham as colunas novas, sem perder dados."""
    colunas = [c["name"] for c in conexao.execute("PRAGMA table_info(produtos)")]
    for coluna in ("embalagem_centavos", "frete_centavos"):
        if coluna not in colunas:
            conexao.execute(
                f"ALTER TABLE produtos ADD COLUMN {coluna} "
                "INTEGER NOT NULL DEFAULT 0"
            )


def inicializar_banco():
    Path(current_app.config["DB_PATH"]).parent.mkdir(parents=True, exist_ok=True)

    with closing(conectar()) as conexao, conexao:
        conexao.execute(SQL_TABELA_PRODUTOS)
        _migrar_para_centavos(conexao)
        _adicionar_coluna_foto(conexao)
        _adicionar_colunas_embalagem_frete(conexao)

        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS multiplicadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                valor REAL NOT NULL
            )
            """
        )

        if not conexao.execute("SELECT 1 FROM multiplicadores LIMIT 1").fetchone():
            conexao.executemany(
                "INSERT INTO multiplicadores (nome, valor) VALUES (?, ?)",
                [
                    ("Básico", 2.5),
                    ("Padrão", 3.0),
                    ("Premium", 3.5),
                    ("Exclusivo", 4.0),
                ],
            )

        if not conexao.execute("SELECT 1 FROM produtos LIMIT 1").fetchone():
            conexao.executemany(
                """
                INSERT INTO produtos
                (nome, categoria, preco_centavos, estoque, descricao)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    ("Notebook Lenovo", "Informática", 350000, 10,
                     "Notebook para estudos e trabalho"),
                    ("Mouse Logitech", "Periféricos", 12000, 25,
                     "Mouse óptico USB"),
                ],
            )