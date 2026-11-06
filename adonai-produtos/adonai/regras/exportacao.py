"""Exportação da lista de produtos para Excel (.xlsx) e CSV.

Só recebe os produtos (dicionários da camada de dados) e devolve bytes.
Não acessa o banco e não conhece rotas.
"""

import csv
import io

from openpyxl import Workbook
from openpyxl.styles import Font

CABECALHO = [
    "ID",
    "Nome",
    "Categoria",
    "Custo",
    "Embalagem",
    "Custo + emb.",
    "Multiplicador",
    "Preço",
    "Estoque",
    "Descrição",
]

# posições (a partir de 0) das colunas em reais
COLUNAS_DINHEIRO = {3, 4, 5, 7}
COLUNA_MULTIPLICADOR = 6

FORMATO_DINHEIRO = '"R$" #,##0.00'
LARGURAS = [6, 30, 18, 12, 12, 14, 14, 12, 10, 40]

# Textos que começam assim podem virar fórmula ao abrir no Excel.
INICIOS_PERIGOSOS = ("=", "+", "-", "@", "\t", "\r")


def montar_linhas(produtos):
    """Uma lista de valores por produto, na mesma ordem do CABECALHO."""
    return [
        [
            produto["id"],
            produto["nome"] or "",
            produto["categoria"] or "",
            produto["custo"],
            produto["embalagem"],
            produto["custo_total"],
            produto["multiplicador"],
            produto["preco"],
            produto["estoque"],
            produto["descricao"] or "",
        ]
        for produto in produtos
    ]


def gerar_xlsx(produtos):
    """Planilha Excel: números ficam como número e textos nunca viram fórmula."""
    pasta = Workbook()
    planilha = pasta.active
    planilha.title = "Produtos"

    planilha.append(CABECALHO)
    for celula in planilha[1]:
        celula.font = Font(bold=True)

    for linha in montar_linhas(produtos):
        planilha.append(linha)

        for indice, celula in enumerate(planilha[planilha.max_row]):
            # o openpyxl trata texto que começa com "=" como fórmula;
            # aqui forçamos "texto" para o Excel nunca executar
            if celula.data_type == "f":
                celula.data_type = "s"
            if indice in COLUNAS_DINHEIRO:
                celula.number_format = FORMATO_DINHEIRO

    for letra, largura in zip("ABCDEFGHIJ", LARGURAS):
        planilha.column_dimensions[letra].width = largura
    planilha.freeze_panes = "A2"

    saida = io.BytesIO()
    pasta.save(saida)
    return saida.getvalue()


def _texto_seguro(texto):
    """No CSV, um apóstrofo na frente impede o Excel de ler como fórmula."""
    if texto and texto[0] in INICIOS_PERIGOSOS:
        return "'" + texto
    return texto


def _celula_csv(valor, indice):
    if indice in COLUNAS_DINHEIRO:
        return f"{valor:.2f}".replace(".", ",")
    if indice == COLUNA_MULTIPLICADOR:
        return str(valor).replace(".", ",")
    if isinstance(valor, str):
        return _texto_seguro(valor)
    return str(valor)


def gerar_csv(produtos):
    """CSV para o Excel brasileiro: separador ';', vírgula decimal, UTF-8 com BOM."""
    saida = io.StringIO()
    escritor = csv.writer(saida, delimiter=";", lineterminator="\r\n")

    escritor.writerow(CABECALHO)
    for linha in montar_linhas(produtos):
        escritor.writerow(
            [_celula_csv(valor, indice) for indice, valor in enumerate(linha)]
        )

    return saida.getvalue().encode("utf-8-sig")
