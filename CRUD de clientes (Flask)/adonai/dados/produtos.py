"""Acesso ao banco: tabela de produtos."""

from contextlib import closing

from adonai.dados import banco
from adonai.regras import dinheiro


def calcular_preco(custo, multiplicador, embalagem=0):
    return dinheiro.calcular_preco(custo, multiplicador, embalagem)


def _produto(linha):
    if linha is None:
        return None
    return {
        "id": linha["id"],
        "nome": linha["nome"],
        "categoria": linha["categoria"],
        "preco": dinheiro.de_centavos(linha["preco_centavos"]),
        "custo": dinheiro.de_centavos(linha["custo_centavos"]),
        "embalagem": dinheiro.de_centavos(linha["embalagem_centavos"]),
        "frete": dinheiro.de_centavos(linha["frete_centavos"]),
        "custo_total": dinheiro.de_centavos(
            linha["custo_centavos"] + linha["embalagem_centavos"]
        ),
        "estoque": linha["estoque"],
        "descricao": linha["descricao"],
        "multiplicador": linha["multiplicador"],
        "foto": linha["foto"],
        "preco_centavos": linha["preco_centavos"],
        "custo_centavos": linha["custo_centavos"],
        "embalagem_centavos": linha["embalagem_centavos"],
        "frete_centavos": linha["frete_centavos"],
    }


def listar_todos():
    with closing(banco.conectar()) as conexao, conexao:
        linhas = conexao.execute(
            "SELECT * FROM produtos ORDER BY nome"
        ).fetchall()
        return [_produto(linha) for linha in linhas]


def buscar_por_id(produto_id):
    with closing(banco.conectar()) as conexao, conexao:
        linha = conexao.execute(
            "SELECT * FROM produtos WHERE id = ?",
            (produto_id,),
        ).fetchone()
        return _produto(linha)


def buscar_por_nome(termo):
    with closing(banco.conectar()) as conexao, conexao:
        linhas = conexao.execute(
            """
            SELECT * FROM produtos
            WHERE nome LIKE ?
            ORDER BY nome
            """,
            (f"%{termo}%",),
        ).fetchall()
        return [_produto(linha) for linha in linhas]


def _preco_final(preco, custo, multiplicador, embalagem=0):
    custo_dec = dinheiro.para_decimal(custo)
    embalagem_dec = dinheiro.para_decimal(embalagem or 0)

    if custo_dec and multiplicador:
        preco_dec = dinheiro.calcular_preco(custo_dec, multiplicador, embalagem_dec)
    else:
        preco_dec = dinheiro.para_decimal(preco)

    return preco_dec, custo_dec, embalagem_dec


def criar(nome, categoria, preco, estoque, descricao, custo=0, multiplicador=0,
          foto=None, embalagem=0, frete=0):
    preco_dec, custo_dec, embalagem_dec = _preco_final(
        preco, custo, multiplicador, embalagem
    )
    frete_dec = dinheiro.para_decimal(frete or 0)

    with closing(banco.conectar()) as conexao, conexao:
        cursor = conexao.execute(
            """
            INSERT INTO produtos
            (nome, categoria, preco_centavos, estoque, descricao,
             custo_centavos, multiplicador, foto,
             embalagem_centavos, frete_centavos)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (nome, categoria, dinheiro.para_centavos(preco_dec), estoque,
             descricao, dinheiro.para_centavos(custo_dec), multiplicador or 0,
             foto, dinheiro.para_centavos(embalagem_dec),
             dinheiro.para_centavos(frete_dec)),
        )
        novo_id = cursor.lastrowid

    return buscar_por_id(novo_id)


def atualizar(produto_id, nome, categoria, preco, estoque, descricao,
              custo=0, multiplicador=0, embalagem=0, frete=0):
    preco_dec, custo_dec, embalagem_dec = _preco_final(
        preco, custo, multiplicador, embalagem
    )
    frete_dec = dinheiro.para_decimal(frete or 0)

    with closing(banco.conectar()) as conexao, conexao:
        conexao.execute(
            """
            UPDATE produtos
            SET nome = ?, categoria = ?, preco_centavos = ?, estoque = ?,
                descricao = ?, custo_centavos = ?, multiplicador = ?,
                embalagem_centavos = ?, frete_centavos = ?
            WHERE id = ?
            """,
            (nome, categoria, dinheiro.para_centavos(preco_dec), estoque,
             descricao, dinheiro.para_centavos(custo_dec), multiplicador or 0,
             dinheiro.para_centavos(embalagem_dec),
             dinheiro.para_centavos(frete_dec), produto_id),
        )

    return buscar_por_id(produto_id)


def definir_foto(produto_id, foto):
    """Troca a foto do produto. Use None para remover."""
    with closing(banco.conectar()) as conexao, conexao:
        conexao.execute(
            "UPDATE produtos SET foto = ? WHERE id = ?",
            (foto, produto_id),
        )
    return buscar_por_id(produto_id)


def excluir(produto_id):
    with closing(banco.conectar()) as conexao, conexao:
        cursor = conexao.execute(
            "DELETE FROM produtos WHERE id = ?",
            (produto_id,),
        )
        return cursor.rowcount > 0