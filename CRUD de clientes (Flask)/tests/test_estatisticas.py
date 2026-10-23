import json
from decimal import Decimal

import pytest

from adonai.regras.estatisticas import calcular_painel


def produto(nome, categoria, preco, estoque, custo="0", embalagem="0"):
    return {
        "nome": nome,
        "categoria": categoria,
        "preco": Decimal(preco),
        "custo": Decimal(custo),
        "custo_total": Decimal(custo) + Decimal(embalagem),
        "estoque": estoque,
    }


def test_sem_produtos_o_painel_fica_zerado():
    dados, resumo = calcular_painel([])

    assert resumo["total_produtos"] == 0
    assert resumo["itens_estoque"] == 0
    assert resumo["valor_estoque"] == 0
    assert resumo["margem_media"] is None
    assert dados["nomes"] == []
    assert dados["custos"] == []


def test_margem_desconta_a_embalagem():
    # preço 62,50; custo 20 + embalagem 5 = 25  ->  margem de 60%
    _, resumo = calcular_painel([produto("Anel", "joia", "62.50", 1, "20", "5")])

    assert resumo["margem_media"] == pytest.approx(60.0)


def test_produto_sem_custo_fica_fora_da_margem_e_do_grafico_de_custos():
    com_custo = produto("Anel", "joia", "62.50", 2, "20", "5")
    sem_custo = produto("Colar", "colar", "10.00", 3)

    dados, resumo = calcular_painel([com_custo, sem_custo])

    assert resumo["margem_media"] == pytest.approx(60.0)
    assert dados["custo_nomes"] == ["Anel"]
    assert dados["custos"] == [25.0]
    assert dados["precos"] == [62.5]
    assert dados["nomes"] == ["Anel", "Colar"]   # o estoque conta todos


def test_valor_do_estoque_soma_preco_vezes_quantidade():
    itens = [produto("A", "x", "62.50", 2, "20", "5"), produto("B", "y", "10.00", 3)]

    _, resumo = calcular_painel(itens)

    assert resumo["itens_estoque"] == 5
    assert resumo["valor_estoque"] == Decimal("155.00")


def test_conta_produtos_por_categoria():
    itens = [
        produto("A", "joia", "1", 1),
        produto("B", "joia", "1", 1),
        produto("C", "anel", "1", 1),
    ]

    dados, _ = calcular_painel(itens)

    assert dados["categorias"] == ["joia", "anel"]
    assert dados["qtd_categorias"] == [2, 1]


def test_dados_dos_graficos_viram_json():
    dados, _ = calcular_painel([produto("Anel", "joia", "62.50", 1, "20", "5")])

    assert json.loads(json.dumps(dados))["custos"] == [25.0]