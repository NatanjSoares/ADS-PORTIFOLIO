from decimal import Decimal

import pytest

import dinheiro


def test_aceita_virgula_e_ponto():
    assert dinheiro.para_decimal("19,90") == Decimal("19.90")
    assert dinheiro.para_decimal("19.90") == Decimal("19.90")


def test_float_impreciso_vira_valor_exato():
    assert dinheiro.para_decimal(0.1 + 0.2) == Decimal("0.30")


def test_centavos_inteiros():
    assert dinheiro.para_centavos("19.99") == 1999
    assert dinheiro.para_centavos(19.99) == 1999
    assert dinheiro.de_centavos(1999) == Decimal("19.99")


def test_soma_de_dez_centavos_e_exata():
    total = sum(dinheiro.para_decimal("0.1") for _ in range(10))
    assert total == Decimal("1.00")


def test_calculo_do_multiplicador():
    assert dinheiro.calcular_preco("20", 2.5) == Decimal("50.00")


def test_arredondamento_meio_para_cima():
    assert dinheiro.calcular_preco("1.01", 2.5) == Decimal("2.53")


@pytest.mark.parametrize("invalido", ["abc", "", "nan", "inf", "100000000"])
def test_valores_invalidos_sao_recusados(invalido):
    with pytest.raises(ValueError):
        dinheiro.para_decimal(invalido)

def test_preco_guardado_em_centavos(produtos):
    from decimal import Decimal

    novo = produtos.criar("Anel", "Joia", 19.99, 1, "x")
    assert novo["preco_centavos"] == 1999
    assert novo["preco"] == Decimal("19.99")


def test_migracao_converte_reais_em_centavos(tmp_path, monkeypatch):
    import importlib
    import sqlite3

    caminho = tmp_path / "antigo.db"
    con = sqlite3.connect(caminho)
    con.execute(
        """
        CREATE TABLE produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL, categoria TEXT NOT NULL,
            preco REAL NOT NULL, estoque INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            custo REAL NOT NULL DEFAULT 0,
            multiplicador REAL NOT NULL DEFAULT 0
        )
        """
    )
    con.execute(
        "INSERT INTO produtos (nome, categoria, preco, estoque, descricao,"
        " custo, multiplicador) VALUES ('Anel','Joia',19.9,2,'x',8.0,2.5)"
    )
    con.commit()
    con.close()

    monkeypatch.setenv("DB_PATH", str(caminho))
    import produtos

    importlib.reload(produtos)

    anel = produtos.buscar_por_nome("Anel")[0]
    assert anel["preco_centavos"] == 1990
    assert anel["custo_centavos"] == 800
    assert anel["estoque"] == 2

def test_embalagem_entra_no_custo_antes_do_multiplicador():
    # (20 + 5) x 2,5 = 62,50
    assert dinheiro.calcular_preco("20", 2.5, embalagem="5") == Decimal("62.50")


def test_sem_embalagem_o_calculo_continua_igual():
    assert dinheiro.calcular_preco("20", 2.5) == Decimal("50.00")
    assert dinheiro.calcular_preco("20", 2.5, embalagem=0) == Decimal("50.00")


def test_embalagem_aceita_virgula():
    assert dinheiro.calcular_preco("10", 2, embalagem="1,50") == Decimal("23.00")


def test_embalagem_invalida_e_recusada():
    with pytest.raises(ValueError):
        dinheiro.calcular_preco("20", 2.5, embalagem="abc")    