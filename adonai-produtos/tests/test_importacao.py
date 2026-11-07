"""Testes da leitura e validação de planilhas de produtos (importação)."""

import io
import zipfile
from decimal import Decimal

import pytest
from openpyxl import Workbook

from adonai.regras import exportacao, importacao

CABECALHO = ["Nome", "Categoria", "Estoque", "Descrição", "Preço"]
ANEL = ["Anel", "Anéis", "3", "Dourado", "29,90"]


def _xlsx(linhas):
    pasta = Workbook()
    planilha = pasta.active
    for linha in linhas:
        planilha.append(linha)
    saida = io.BytesIO()
    pasta.save(saida)
    return saida.getvalue()


def _csv(texto, codificacao="utf-8-sig"):
    return texto.encode(codificacao)


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


def test_le_xlsx_com_custo_e_multiplicador():
    arquivo = _xlsx([
        ["Nome", "Categoria", "Custo", "Embalagem", "Multiplicador",
         "Estoque", "Descrição"],
        ["Anel", "Anéis", 10, 2, 2.5, 7, "Dourado"],
    ])

    resultado = importacao.ler_produtos("lista.xlsx", arquivo)

    assert resultado.erros == []
    assert resultado.produtos == [{
        "nome": "Anel",
        "categoria": "Anéis",
        "preco": Decimal("30.00"),
        "estoque": 7,
        "descricao": "Dourado",
        "custo": Decimal("10.00"),
        "multiplicador": 2.5,
        "embalagem": Decimal("2.00"),
        "frete": 0,
    }]


def test_ida_e_volta_pelo_xlsx_da_exportacao():
    arquivo = exportacao.gerar_xlsx([_produto()])

    resultado = importacao.ler_produtos("produtos.xlsx", arquivo)

    assert resultado.erros == []
    produto = resultado.produtos[0]
    assert produto["nome"] == "Brinco"
    assert produto["preco"] == Decimal("30.00")
    assert produto["custo"] == Decimal("10.00")
    assert produto["multiplicador"] == 2.5
    assert produto["estoque"] == 7


def test_ida_e_volta_pelo_csv_da_exportacao():
    arquivo = exportacao.gerar_csv([_produto()])

    resultado = importacao.ler_produtos("produtos.csv", arquivo)

    assert resultado.erros == []
    produto = resultado.produtos[0]
    assert produto["nome"] == "Brinco"
    assert produto["preco"] == Decimal("30.00")
    assert produto["multiplicador"] == 2.5


def test_ida_e_volta_de_produto_so_com_preco():
    zero = Decimal("0.00")
    produto = _produto(
        nome="Notebook",
        custo=zero,
        embalagem=zero,
        custo_total=zero,
        multiplicador=0,
        preco=Decimal("3500.00"),
    )

    resultado = importacao.ler_produtos(
        "produtos.csv", exportacao.gerar_csv([produto])
    )

    assert resultado.erros == []
    assert resultado.produtos[0]["preco"] == Decimal("3500.00")
    assert resultado.produtos[0]["custo"] == 0


def test_acha_o_cabecalho_depois_de_linhas_de_titulo():
    arquivo = _xlsx([["Meus produtos"], [None], CABECALHO, ANEL])

    resultado = importacao.ler_produtos("lista.xlsx", arquivo)

    assert [p["nome"] for p in resultado.produtos] == ["Anel"]
    assert resultado.produtos[0]["preco"] == Decimal("29.90")


def test_erro_aponta_a_linha_do_arquivo_e_nao_impede_ler_as_outras():
    arquivo = _xlsx([
        CABECALHO,
        ANEL,
        [None],
        ["Colar", "Colares", "abc", "Prata", "40"],
    ])

    resultado = importacao.ler_produtos("lista.xlsx", arquivo)

    assert len(resultado.produtos) == 1
    assert resultado.erros == ["Linha 4: Informe um estoque válido."]
    assert resultado.ignorados == []


def test_ignora_nome_que_ja_existe_e_nome_repetido_na_planilha():
    arquivo = _xlsx([
        CABECALHO,
        ["Anel", "Anéis", "1", "Dourado", "10"],
        ["ANEL ", "Anéis", "1", "Dourado", "10"],
        ["Brinco", "Brincos", "1", "Dourado", "10"],
    ])

    resultado = importacao.ler_produtos(
        "lista.xlsx", arquivo, nomes_existentes={"brinco"}
    )

    assert [p["nome"] for p in resultado.produtos] == ["Anel"]
    assert len(resultado.ignorados) == 2
    assert resultado.ignorados[0].startswith("Linha 3:")
    assert resultado.ignorados[1].startswith("Linha 4:")


def test_le_csv_com_ponto_e_virgula_e_windows_1252():
    texto = "Nome;Categoria;Estoque;Descrição;Preço\nAnel;Anéis;3;Dourado;29,90\n"

    resultado = importacao.ler_produtos("lista.csv", _csv(texto, "cp1252"))

    assert resultado.produtos[0]["categoria"] == "Anéis"
    assert resultado.produtos[0]["preco"] == Decimal("29.90")


def test_le_csv_com_virgula_e_ponto_decimal():
    texto = "Nome,Categoria,Estoque,Descrição,Preço\nAnel,Anéis,3,Dourado,29.90\n"

    resultado = importacao.ler_produtos("lista.csv", _csv(texto))

    assert resultado.produtos[0]["preco"] == Decimal("29.90")


def test_tira_o_apostrofo_que_a_exportacao_poe_antes_de_formulas():
    texto = "Nome;Categoria;Estoque;Descrição;Preço\n'=1+1;Teste;1;Descrição;10\n"

    resultado = importacao.ler_produtos("lista.csv", _csv(texto))

    assert resultado.produtos[0]["nome"] == "=1+1"


def test_recusa_arquivo_sem_coluna_obrigatoria():
    with pytest.raises(importacao.ErroDeImportacao, match="Categoria"):
        importacao.ler_produtos("lista.csv", _csv("Nome;Estoque\nAnel;1\n"))


def test_recusa_extensao_desconhecida():
    for nome in ("lista.pdf", "lista.xlsm", "lista"):
        with pytest.raises(importacao.ErroDeImportacao, match=r"\.xlsx"):
            importacao.ler_produtos(nome, b"conteudo")


def test_recusa_arquivo_grande_demais():
    conteudo = b"x" * (importacao.TAMANHO_MAXIMO + 1)

    with pytest.raises(importacao.ErroDeImportacao, match="grande demais"):
        importacao.ler_produtos("lista.csv", conteudo)


def test_recusa_planilha_com_linhas_demais(monkeypatch):
    monkeypatch.setattr(importacao, "LINHAS_MAXIMAS", 2)
    texto = "Nome;Categoria;Estoque;Descrição;Preço\n" + "A;B;1;D;10\n" * 3

    with pytest.raises(importacao.ErroDeImportacao, match="mais de 2"):
        importacao.ler_produtos("lista.csv", _csv(texto))


def test_recusa_xlsx_que_nao_e_uma_planilha():
    with pytest.raises(importacao.ErroDeImportacao, match="abrir"):
        importacao.ler_produtos("lista.xlsx", b"isso nao e uma planilha")


def test_recusa_planilha_com_macro():
    saida = io.BytesIO()
    with zipfile.ZipFile(saida, "w") as arquivo:
        arquivo.writestr("xl/vbaProject.bin", b"x")

    with pytest.raises(importacao.ErroDeImportacao, match="macro"):
        importacao.ler_produtos("lista.xlsx", saida.getvalue())


def test_recusa_xlsx_que_incha_demais_ao_abrir(monkeypatch):
    monkeypatch.setattr(importacao, "LIMITE_DESCOMPACTADO", 10)

    with pytest.raises(importacao.ErroDeImportacao, match="grande demais"):
        importacao.ler_produtos("lista.xlsx", _xlsx([CABECALHO, ANEL]))


def test_recusa_zip_que_nao_e_planilha():
    saida = io.BytesIO()
    with zipfile.ZipFile(saida, "w") as arquivo:
        arquivo.writestr("qualquer.txt", b"x")

    with pytest.raises(importacao.ErroDeImportacao, match="abrir"):
        importacao.ler_produtos("lista.xlsx", saida.getvalue())
