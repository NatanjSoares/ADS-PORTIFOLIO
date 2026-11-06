"""Testes da exportação de produtos (xlsx e csv)."""

import csv
import io
from decimal import Decimal

from openpyxl import load_workbook

from adonai.regras import exportacao

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


def _produto(**mudancas):
    produto = {
        "id": 1,
        "nome": "Brinco",
        "categoria": "Brincos",
        "custo": Decimal("10.00"),
        "embalagem": Decimal("2.00"),
        "custo_total": Decimal("12.00"),
        "multiplicador": 2.5,
        "preco": Decimal("30.00"),
        "estoque": 7,
        "descricao": "Dourado",
    }
    produto.update(mudancas)
    return produto


def _abrir_xlsx(dados):
    return load_workbook(io.BytesIO(dados)).active


def _ler_csv(dados):
    texto = dados.decode("utf-8-sig")
    return list(csv.reader(io.StringIO(texto), delimiter=";"))


def test_linhas_mantem_a_ordem_dos_produtos():
    linhas = exportacao.montar_linhas(
        [_produto(id=1, nome="A"), _produto(id=2, nome="B")]
    )

    assert [linha[1] for linha in linhas] == ["A", "B"]


def test_xlsx_tem_cabecalho_na_primeira_linha():
    planilha = _abrir_xlsx(exportacao.gerar_xlsx([_produto()]))

    assert [c.value for c in planilha[1]] == CABECALHO


def test_xlsx_guarda_numeros_como_numeros():
    planilha = _abrir_xlsx(exportacao.gerar_xlsx([_produto()]))
    linha = [c.value for c in planilha[2]]

    assert linha[0] == 1
    assert float(linha[3]) == 10.0
    assert float(linha[7]) == 30.0
    assert not isinstance(linha[7], str)
    assert linha[6] == 2.5
    assert linha[8] == 7


def test_xlsx_sem_produtos_so_tem_cabecalho():
    planilha = _abrir_xlsx(exportacao.gerar_xlsx([]))

    assert planilha.max_row == 1


def test_xlsx_nao_executa_formula_digitada_no_nome():
    planilha = _abrir_xlsx(exportacao.gerar_xlsx([_produto(nome="=1+1")]))
    celula = planilha["B2"]

    assert celula.value == "=1+1"
    assert celula.data_type == "s"


def test_xlsx_descricao_vazia_vira_celula_vazia():
    planilha = _abrir_xlsx(exportacao.gerar_xlsx([_produto(descricao=None)]))

    assert not planilha["J2"].value


def test_csv_comeca_com_bom_utf8():
    dados = exportacao.gerar_csv([_produto()])

    assert dados.startswith(b"\xef\xbb\xbf")


def test_csv_usa_ponto_e_virgula_e_virgula_decimal():
    produto = _produto(
        categoria="Pulseiras",
        descricao="Folheado a ouro; não alérgico",
    )

    linhas = _ler_csv(exportacao.gerar_csv([produto]))

    assert linhas[0] == CABECALHO
    assert linhas[1] == [
        "1", "Brinco", "Pulseiras", "10,00", "2,00", "12,00",
        "2,5", "30,00", "7", "Folheado a ouro; não alérgico",
    ]


def test_csv_neutraliza_textos_que_virariam_formula():
    for inicio in ("=", "+", "-", "@"):
        nome = f"{inicio}1+1"

        linhas = _ler_csv(exportacao.gerar_csv([_produto(nome=nome)]))

        assert linhas[1][1] == "'" + nome


def test_csv_sem_produtos_so_tem_cabecalho():
    linhas = _ler_csv(exportacao.gerar_csv([]))

    assert linhas == [CABECALHO]
