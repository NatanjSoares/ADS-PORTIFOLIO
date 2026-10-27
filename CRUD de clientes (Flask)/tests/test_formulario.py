"""campos_do_produto: converte o formulário nos campos que o banco recebe."""

from decimal import Decimal

from ajudantes import _dados
from adonai.regras.validacao import campos_do_produto

CHAVES = {
    "nome", "categoria", "preco", "estoque", "descricao",
    "custo", "multiplicador", "embalagem", "frete",
}


def test_formulario_minimo_vira_os_campos_do_produto():
    campos = campos_do_produto(_dados(
        nome="  Anel  ", categoria=" Joia ", descricao=" x ", estoque="3",
    ))

    assert campos["nome"] == "Anel"
    assert campos["categoria"] == "Joia"
    assert campos["descricao"] == "x"
    assert campos["estoque"] == 3
    assert campos["preco"] == Decimal("10")


def test_campos_opcionais_vazios_viram_zero():
    campos = campos_do_produto(_dados())

    assert campos["custo"] == 0
    assert campos["multiplicador"] == 0
    assert campos["embalagem"] == 0
    assert campos["frete"] == 0


def test_preco_sai_do_calculo_quando_ha_custo_e_multiplicador():
    campos = campos_do_produto(_dados(
        custo="20", multiplicador="2.5", embalagem="5",
    ))

    assert campos["preco"] == Decimal("62.50")  # (20 + 5) x 2,5
    assert campos["custo"] == 20
    assert campos["multiplicador"] == 2.5
    assert campos["embalagem"] == 5


def test_frete_com_virgula_e_entendido():
    campos = campos_do_produto(_dados(frete="12,90"))

    assert campos["frete"] == Decimal("12.90")


def test_devolve_exatamente_os_campos_do_produto_sem_a_foto():
    campos = campos_do_produto(_dados())

    assert set(campos) == CHAVES
    assert "foto" not in campos