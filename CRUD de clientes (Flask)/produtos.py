import os
import sqlite3
from contextlib import closing
from pathlib import Path


caminho_banco = Path(
    os.environ.get("DB_PATH", Path(__file__).parent / "produtos.db")
)
caminho_banco.parent.mkdir(parents=True, exist_ok=True)

MULT_MIN, MULT_MAX = 1.5, 4.0


def calcular_preco(custo, multiplicador):
    return round(custo * multiplicador, 2)


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

        colunas = [
            c["name"] for c in conexao.execute("PRAGMA table_info(produtos)")
        ]
        if "custo" not in colunas:
            conexao.execute(
                "ALTER TABLE produtos ADD COLUMN custo REAL NOT NULL DEFAULT 0"
            )
        if "multiplicador" not in colunas:
            conexao.execute(
                "ALTER TABLE produtos ADD COLUMN multiplicador REAL NOT NULL DEFAULT 0"
            )

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


def criar(nome, categoria, preco, estoque, descricao, custo=0, multiplicador=0):
    if custo and multiplicador:
        preco = calcular_preco(custo, multiplicador)

    with closing(_conectar()) as conexao, conexao:
        cursor = conexao.execute(
            """
            INSERT INTO produtos
            (nome, categoria, preco, estoque, descricao, custo, multiplicador)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (nome, categoria, preco, estoque, descricao, custo, multiplicador),
        )
        novo_id = cursor.lastrowid

    return buscar_por_id(novo_id)


def atualizar(produto_id, nome, categoria, preco, estoque, descricao,
              custo=0, multiplicador=0):
    if custo and multiplicador:
        preco = calcular_preco(custo, multiplicador)

    with closing(_conectar()) as conexao, conexao:
        conexao.execute(
            """
            UPDATE produtos
            SET nome = ?, categoria = ?, preco = ?, estoque = ?,
                descricao = ?, custo = ?, multiplicador = ?
            WHERE id = ?
            """,
            (nome, categoria, preco, estoque, descricao,
             custo, multiplicador, produto_id),
        )

    return buscar_por_id(produto_id)


def excluir(produto_id):
    with closing(_conectar()) as conexao, conexao:
        cursor = conexao.execute(
            "DELETE FROM produtos WHERE id = ?",
            (produto_id,),
        )
        return cursor.rowcount > 0


def listar_multiplicadores():
    with closing(_conectar()) as conexao, conexao:
        linhas = conexao.execute(
            "SELECT * FROM multiplicadores ORDER BY valor"
        ).fetchall()
        return [dict(linha) for linha in linhas]


def criar_multiplicador(nome, valor):
    with closing(_conectar()) as conexao, conexao:
        conexao.execute(
            "INSERT INTO multiplicadores (nome, valor) VALUES (?, ?)",
            (nome, valor),
        )


def atualizar_multiplicador(mult_id, nome, valor):
    with closing(_conectar()) as conexao, conexao:
        conexao.execute(
            "UPDATE multiplicadores SET nome = ?, valor = ? WHERE id = ?",
            (nome, valor, mult_id),
        )


def excluir_multiplicador(mult_id):
    with closing(_conectar()) as conexao, conexao:
        conexao.execute("DELETE FROM multiplicadores WHERE id = ?", (mult_id,))


inicializar_banco()