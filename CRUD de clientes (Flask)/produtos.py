import os
import sqlite3
from contextlib import closing
from pathlib import Path

import dinheiro


caminho_banco = Path(
    os.environ.get("DB_PATH", Path(__file__).parent / "produtos.db")
)
caminho_banco.parent.mkdir(parents=True, exist_ok=True)

MULT_MIN, MULT_MAX = 1.5, 4.0

SQL_TABELA_PRODUTOS = """
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        categoria TEXT NOT NULL,
        preco_centavos INTEGER NOT NULL,
        estoque INTEGER NOT NULL,
        descricao TEXT NOT NULL,
        custo_centavos INTEGER NOT NULL DEFAULT 0,
        multiplicador REAL NOT NULL DEFAULT 0
    )
"""


def calcular_preco(custo, multiplicador):
    return dinheiro.calcular_preco(custo, multiplicador)


def _conectar():
    conexao = sqlite3.connect(caminho_banco)
    conexao.row_factory = sqlite3.Row
    return conexao


def _produto(linha):
    if linha is None:
        return None
    return {
        "id": linha["id"],
        "nome": linha["nome"],
        "categoria": linha["categoria"],
        "preco": dinheiro.de_centavos(linha["preco_centavos"]),
        "custo": dinheiro.de_centavos(linha["custo_centavos"]),
        "estoque": linha["estoque"],
        "descricao": linha["descricao"],
        "multiplicador": linha["multiplicador"],
        "preco_centavos": linha["preco_centavos"],
        "custo_centavos": linha["custo_centavos"],
    }


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


def inicializar_banco():
    with closing(_conectar()) as conexao, conexao:
        conexao.execute(SQL_TABELA_PRODUTOS)
        _migrar_para_centavos(conexao)

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


def listar_todos():
    with closing(_conectar()) as conexao, conexao:
        linhas = conexao.execute(
            "SELECT * FROM produtos ORDER BY nome"
        ).fetchall()
        return [_produto(linha) for linha in linhas]


def buscar_por_id(produto_id):
    with closing(_conectar()) as conexao, conexao:
        linha = conexao.execute(
            "SELECT * FROM produtos WHERE id = ?",
            (produto_id,),
        ).fetchone()
        return _produto(linha)


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
        return [_produto(linha) for linha in linhas]


def _preco_final(preco, custo, multiplicador):
    custo_dec = dinheiro.para_decimal(custo)
    if custo_dec and multiplicador:
        preco_dec = dinheiro.calcular_preco(custo_dec, multiplicador)
    else:
        preco_dec = dinheiro.para_decimal(preco)
    return preco_dec, custo_dec


def criar(nome, categoria, preco, estoque, descricao, custo=0, multiplicador=0):
    preco_dec, custo_dec = _preco_final(preco, custo, multiplicador)

    with closing(_conectar()) as conexao, conexao:
        cursor = conexao.execute(
            """
            INSERT INTO produtos
            (nome, categoria, preco_centavos, estoque, descricao,
             custo_centavos, multiplicador)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (nome, categoria, dinheiro.para_centavos(preco_dec), estoque,
             descricao, dinheiro.para_centavos(custo_dec), multiplicador or 0),
        )
        novo_id = cursor.lastrowid

    return buscar_por_id(novo_id)


def atualizar(produto_id, nome, categoria, preco, estoque, descricao,
              custo=0, multiplicador=0):
    preco_dec, custo_dec = _preco_final(preco, custo, multiplicador)

    with closing(_conectar()) as conexao, conexao:
        conexao.execute(
            """
            UPDATE produtos
            SET nome = ?, categoria = ?, preco_centavos = ?, estoque = ?,
                descricao = ?, custo_centavos = ?, multiplicador = ?
            WHERE id = ?
            """,
            (nome, categoria, dinheiro.para_centavos(preco_dec), estoque,
             descricao, dinheiro.para_centavos(custo_dec), multiplicador or 0,
             produto_id),
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