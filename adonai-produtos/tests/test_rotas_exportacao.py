"""Testes da rota de exportação de produtos."""

import io

from openpyxl import load_workbook

XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def _esvaziar(produtos):
    """Apaga os produtos de exemplo que o banco de teste já traz."""
    for produto in produtos.listar_todos():
        produtos.excluir(produto["id"])


def _criar(produtos, nome, categoria="Brincos"):
    produtos.criar(
        nome=nome,
        categoria=categoria,
        preco=30,
        estoque=5,
        descricao="Teste",
    )


def _nomes_do_xlsx(resposta):
    planilha = load_workbook(io.BytesIO(resposta.data)).active
    return [linha[1] for linha in planilha.iter_rows(min_row=2, values_only=True)]


def test_exportar_xlsx_baixa_o_arquivo(client, produtos):
    _esvaziar(produtos)
    _criar(produtos, "Brinco")

    resposta = client.get("/produtos/exportar/xlsx")

    assert resposta.status_code == 200
    assert resposta.mimetype == XLSX
    assert resposta.headers["Cache-Control"] == "no-store"
    disposicao = resposta.headers["Content-Disposition"]
    assert disposicao.startswith('attachment; filename="produtos-')
    assert disposicao.endswith('.xlsx"')
    assert _nomes_do_xlsx(resposta) == ["Brinco"]


def test_exportar_csv_baixa_o_arquivo(client, produtos):
    _criar(produtos, "Brinco")

    resposta = client.get("/produtos/exportar/csv")

    assert resposta.status_code == 200
    assert resposta.mimetype == "text/csv"
    assert resposta.headers["Content-Disposition"].endswith('.csv"')
    assert resposta.data.startswith(b"\xef\xbb\xbf")
    assert "Brinco" in resposta.data.decode("utf-8-sig")


def test_exportar_sem_busca_traz_todos_em_ordem_de_nome(client, produtos):
    _esvaziar(produtos)
    _criar(produtos, "Colar")
    _criar(produtos, "Anel")

    resposta = client.get("/produtos/exportar/xlsx")

    assert _nomes_do_xlsx(resposta) == ["Anel", "Colar"]


def test_exportar_respeita_a_busca_da_lista(client, produtos):
    _criar(produtos, "Anel dourado")
    _criar(produtos, "Colar prata")

    resposta = client.get("/produtos/exportar/xlsx?q=anel")

    assert _nomes_do_xlsx(resposta) == ["Anel dourado"]


def test_exportar_sem_produtos_devolve_so_o_cabecalho(client, produtos):
    _esvaziar(produtos)

    resposta = client.get("/produtos/exportar/xlsx")

    assert resposta.status_code == 200
    assert _nomes_do_xlsx(resposta) == []


def test_exportar_formato_desconhecido_da_404(client):
    resposta = client.get("/produtos/exportar/pdf")

    assert resposta.status_code == 404


def test_exportar_exige_login(client_anonimo):
    resposta = client_anonimo.get("/produtos/exportar/xlsx")

    assert resposta.status_code == 302
    assert "login" in resposta.headers["Location"]
