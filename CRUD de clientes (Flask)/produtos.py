import os
import sqlite3
from contextlib import closing
from pathlib import Path


caminho_banco = Path(
    os.environ.get("DB_PATH", Path(__file__).parent / "produtos.db")
)
caminho_banco.parent.mkdir(parents=True, exist_ok=True)


def _conectar():
    conexao = sqlite3.connect(caminho_banco)
    conexao.row_factory = sqlite3.Row
    return conexao


def inicializar_banco():
    with closing(_conectar()) as conexao, conexao:
        conexao.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                preco REAL NOT NULL,
                estoque INTEGER NOT NULL,
                descricao TEXT NOT NULL
            )
            """
        )

        existe_algum = conexao.execute(
            "SELECT 1 FROM produtos LIMIT 1"
        ).fetchone()

        if not existe_algum:
            conexao.executemany(
                """
                INSERT INTO produtos
                (nome, categoria, preco, estoque, descricao)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (
                        "Notebook Lenovo",
                        "Informática",
                        3500.00,
                        10,
                        "Notebook para estudos e trabalho",
                    ),
                    (
                        "Mouse Logitech",
                        "Periféricos",
                        120.00,
                        25,
                        "Mouse óptico USB",
                    ),
                ],
            )


def listar_todos():
    with closing(_conectar()) as conexao, conexao:
        linhas = conexao.execute(
            "SELECT * FROM produtos ORDER BY nome"
        ).fetchall()

        return [dict(linha) for linha in linhas]


def buscar_por_id(produto_id):
    with closing(_conectar()) as conexao, conexao:
        linha = conexao.execute(
            "SELECT * FROM produtos WHERE id = ?",
            (produto_id,),
        ).fetchone()

        return dict(linha) if linha else None


def buscar_por_nome(termo):
    with closing(_conectar()) as conexao, conexao:
        linhas = conexao.execute(
            """
            SELECT * FROM produtos
            WHERE nome LIKE ?
            ORDER BY nome
            """,
            (f"%{termo}%",),
        ).fetchall()

        return [dict(linha) for linha in linhas]


def criar(nome, categoria, preco, estoque, descricao):
    with closing(_conectar()) as conexao, conexao:
        cursor = conexao.execute(
            """
            INSERT INTO produtos
            (nome, categoria, preco, estoque, descricao)
            VALUES (?, ?, ?, ?, ?)
            """,
            (nome, categoria, preco, estoque, descricao),
        )

        novo_id = cursor.lastrowid

    return buscar_por_id(novo_id)


def atualizar(produto_id, nome, categoria, preco, estoque, descricao):
    with closing(_conectar()) as conexao, conexao:
        conexao.execute(
            """
            UPDATE produtos
            SET nome = ?,
                categoria = ?,
                preco = ?,
                estoque = ?,
                descricao = ?
            WHERE id = ?
            """,
            (nome, categoria, preco, estoque, descricao, produto_id),
        )

    return buscar_por_id(produto_id)


def excluir(produto_id):
    with closing(_conectar()) as conexao, conexao:
        cursor = conexao.execute(
            "DELETE FROM produtos WHERE id = ?",
            (produto_id,),
        )

        return cursor.rowcount > 0


inicializar_banco()