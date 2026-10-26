"""Acesso ao banco: tabela de multiplicadores."""

from contextlib import closing

from adonai.dados import banco


def listar_multiplicadores():
    with closing(banco.conectar()) as conexao, conexao:
        linhas = conexao.execute(
            "SELECT * FROM multiplicadores ORDER BY valor"
        ).fetchall()
        return [dict(linha) for linha in linhas]


def criar_multiplicador(nome, valor):
    with closing(banco.conectar()) as conexao, conexao:
        conexao.execute(
            "INSERT INTO multiplicadores (nome, valor) VALUES (?, ?)",
            (nome, valor),
        )


def atualizar_multiplicador(mult_id, nome, valor):
    with closing(banco.conectar()) as conexao, conexao:
        conexao.execute(
            "UPDATE multiplicadores SET nome = ?, valor = ? WHERE id = ?",
            (nome, valor, mult_id),
        )


def excluir_multiplicador(mult_id):
    with closing(banco.conectar()) as conexao, conexao:
        conexao.execute("DELETE FROM multiplicadores WHERE id = ?", (mult_id,))