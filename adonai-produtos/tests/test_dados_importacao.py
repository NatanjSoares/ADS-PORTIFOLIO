"""Testes da gravação em lote usada pela importação de produtos."""

import sqlite3
from decimal import Decimal

import pytest

from adonai.dados import produtos as dados
from adonai.regras import importacao


def _item(nome, **mudancas):
    item = {
        "nome": nome,
        "categoria": "Brincos",
        "preco": Decimal("30.00"),
        "estoque": 5,
        "descricao": "Teste",
        "custo": 0,
        "multiplicador": 0,
        "embalagem": 0,
        "frete": 0,
    }
    item.update(mudancas)
    return item


@pytest.mark.usefixtures("produtos")
def test_criar_varios_grava_todos():
    antes = len(dados.listar_todos())

    gravados = dados.criar_varios([_item("Anel"), _item("Colar")])

    assert gravados == 2
    assert len(dados.listar_todos()) == antes + 2


@pytest.mark.usefixtures("produtos")
def test_criar_varios_com_lista_vazia_nao_grava_nada():
    antes = len(dados.listar_todos())

    assert dados.criar_varios([]) == 0
    assert len(dados.listar_todos()) == antes


@pytest.mark.usefixtures("produtos")
def test_criar_varios_calcula_o_preco_como_o_cadastro():
    dados.criar_varios([
        _item(
            "Anel",
            preco=Decimal("0.00"),
            custo=Decimal("10.00"),
            embalagem=Decimal("2.00"),
            multiplicador=2.5,
        ),
    ])

    anel = dados.buscar_por_nome("Anel")[0]

    assert anel["preco"] == Decimal("30.00")
    assert anel["custo_total"] == Decimal("12.00")
    assert anel["multiplicador"] == 2.5


@pytest.mark.usefixtures("produtos")
def test_criar_varios_e_tudo_ou_nada():
    antes = len(dados.listar_todos())

    with pytest.raises(sqlite3.IntegrityError):
        dados.criar_varios([_item("Anel"), _item(None)])

    assert len(dados.listar_todos()) == antes
    assert dados.buscar_por_nome("Anel") == []


@pytest.mark.usefixtures("produtos")
def test_nomes_cadastrados_lista_os_nomes_que_existem():
    dados.criar_varios([_item("Anel")])

    nomes = dados.nomes_cadastrados()

    assert "Anel" in nomes
    assert sorted(nomes) == sorted(p["nome"] for p in dados.listar_todos())


@pytest.mark.usefixtures("produtos")
def test_produtos_lidos_da_planilha_podem_ser_gravados():
    texto = (
        "Nome;Categoria;Custo;Multiplicador;Estoque;Descrição\n"
        "Anel;Anéis;10;2,5;4;Dourado\n"
    )

    resultado = importacao.ler_produtos(
        "lista.csv", texto.encode("utf-8-sig"), dados.nomes_cadastrados()
    )
    dados.criar_varios(resultado.produtos)

    anel = dados.buscar_por_nome("Anel")[0]

    assert resultado.erros == []
    assert anel["preco"] == Decimal("25.00")
    assert anel["estoque"] == 4
