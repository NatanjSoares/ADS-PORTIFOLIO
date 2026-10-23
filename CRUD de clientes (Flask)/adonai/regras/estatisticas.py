"""Cálculos do dashboard (sem Flask e sem banco, para testar de forma simples)."""


def calcular_painel(produtos):
    """Recebe a lista de produtos e devolve (dados_dos_graficos, resumo)."""
    com_custo = [p for p in produtos if p["custo"]]

    categorias = {}
    for p in produtos:
        categorias[p["categoria"]] = categorias.get(p["categoria"], 0) + 1

    margens = [
        (p["preco"] - p["custo_total"]) / p["preco"] * 100
        for p in com_custo
        if p["preco"]
    ]

    dados = {
        "nomes": [p["nome"] for p in produtos],
        "estoque": [p["estoque"] for p in produtos],
        "custo_nomes": [p["nome"] for p in com_custo],
        "custos": [float(p["custo_total"]) for p in com_custo],
        "precos": [float(p["preco"]) for p in com_custo],
        "categorias": list(categorias.keys()),
        "qtd_categorias": list(categorias.values()),
    }

    resumo = {
        "total_produtos": len(produtos),
        "itens_estoque": sum(p["estoque"] for p in produtos),
        "valor_estoque": sum(p["preco"] * p["estoque"] for p in produtos),
        "margem_media": sum(margens) / len(margens) if margens else None,
    }

    return dados, resumo