from decimal import Decimal

import pytest

from adonai.regras.validacao import (
    decimal_ou_none,
    numero_ou_none,
    preco_do_formulario,
    validar_formulario,
)

BASE = {
    "nome": "Anel",
    "categoria": "Joia",
    "preco": "10",
    "estoque": "1",
    "descricao": "x",
}

CASOS = [
    ({"nome": ""}, "nome do produto é obrigatório"),
    ({"categoria": ""}, "categoria é obrigatória"),
    ({"preco": ""}, "preço é obrigatório"),
    ({"preco": "abc"}, "preço válido"),
    ({"preco": "-5"}, "preço não pode ser negativo"),
    ({"custo": "abc", "multiplicador": "2.5"}, "custo válido"),
    ({"custo": "20", "multiplicador": "5"}, "entre 1,5 e 4"),
    ({"custo": "20", "multiplicador": "1"}, "entre 1,5 e 4"),
    ({"custo": "20"}, "entre 1,5 e 4"),
    ({"embalagem": "abc"}, "valor válido para a embalagem"),
    ({"embalagem": "-1"}, "embalagem não pode ser negativa"),
    ({"frete": "abc"}, "valor válido para o frete"),
    ({"frete": "-5"}, "frete não pode ser negativo"),
    ({"estoque": ""}, "estoque é obrigatório"),
    ({"estoque": "-1"}, "estoque não pode ser negativo"),
    ({"estoque": "abc"}, "estoque válido"),
    ({"descricao": ""}, "descrição é obrigatória"),
]


@pytest.mark.parametrize("texto, esperado", [
    ("2.5", 2.5), ("3", 3.0), ("abc", None), ("", None), (None, None),
])
def test_numero_ou_none(texto, esperado):
    assert numero_ou_none(texto) == esperado


@pytest.mark.parametrize("texto, esperado", [
    ("19,90", Decimal("19.90")),
    ("19.90", Decimal("19.90")),
    ("abc", None),
    ("", None),
    ("nan", None),
])
def test_decimal_ou_none(texto, esperado):
    assert decimal_ou_none(texto) == esperado


def test_formulario_valido_nao_tem_erro():
    assert validar_formulario(BASE) is None


def test_formulario_valido_com_multiplicador_embalagem_e_frete():
    form = {**BASE, "custo": "20", "multiplicador": "2.5",
            "embalagem": "5", "frete": "12,90"}
    assert validar_formulario(form) is None


@pytest.mark.parametrize("mudanca, trecho", CASOS)
def test_formulario_invalido_mostra_o_erro_certo(mudanca, trecho):
    erro = validar_formulario({**BASE, **mudanca})

    assert erro is not None
    assert trecho in erro


def test_preco_calculado_com_embalagem():
    form = {"custo": "20", "multiplicador": "2.5", "embalagem": "5"}
    assert preco_do_formulario(form) == Decimal("62.50")


def test_preco_calculado_sem_embalagem():
    form = {"custo": "20", "multiplicador": "2.5"}
    assert preco_do_formulario(form) == Decimal("50.00")


def test_preco_manual_quando_nao_ha_multiplicador():
    assert preco_do_formulario({"preco": "10"}) == Decimal("10.00")


def test_frete_nao_entra_no_preco():
    form = {"custo": "20", "multiplicador": "2.5", "embalagem": "5", "frete": "100"}
    assert preco_do_formulario(form) == Decimal("62.50")


def test_preco_vazio_devolve_none():
    assert preco_do_formulario({}) is None