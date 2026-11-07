"""Importação de produtos a partir de planilha (.xlsx) ou CSV.

Só lê e confere o arquivo: não acessa o banco, não conhece rotas e nunca
grava nada. Quem decide o que fazer com o resultado é a rota.

Formato aceito (o mesmo que a exportação gera): uma linha de cabeçalho com
as colunas Nome, Categoria, Estoque e Descrição, mais Preço ou então
Custo e Multiplicador. Embalagem e Frete são opcionais. As colunas ID e
"Custo + emb." são ignoradas. Em .xlsx, só a primeira aba é lida.
"""

import csv
import io
import unicodedata
import zipfile
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from itertools import islice

from openpyxl import load_workbook

from adonai.regras.exportacao import INICIOS_PERIGOSOS
from adonai.regras.validacao import campos_do_produto, validar_formulario

TAMANHO_MAXIMO = 2 * 1024 * 1024  # arquivo enviado: 2 MB
LIMITE_DESCOMPACTADO = 20 * 1024 * 1024  # o .xlsx "por dentro": 20 MB
LINHAS_MAXIMAS = 1000  # produtos por arquivo
LINHAS_DE_CABECALHO = 10  # quantas linhas do topo olhar para achar o cabeçalho
COLUNAS_MAXIMAS = 40

OBRIGATORIAS = ("nome", "categoria", "estoque", "descricao")
CAMPOS = (
    "nome",
    "categoria",
    "custo",
    "embalagem",
    "multiplicador",
    "preco",
    "estoque",
    "descricao",
    "frete",
)

MENSAGEM_ABRIR = "Não consegui abrir a planilha. Confira se é um .xlsx válido."


class ErroDeImportacao(Exception):
    """Problema com o arquivo inteiro (formato, tamanho ou colunas)."""


@dataclass
class ResultadoImportacao:
    produtos: list = field(default_factory=list)  # prontos para produtos.criar
    erros: list = field(default_factory=list)  # "Linha 7: ..."
    ignorados: list = field(default_factory=list)  # nomes repetidos ou já cadastrados


def _normalizar(texto):
    """Minúsculas, sem acento e sem espaços sobrando: ' Preço ' -> 'preco'."""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return " ".join(texto.casefold().split())


def _texto(valor):
    """Valor de uma célula como texto simples ('' se vazia)."""
    if valor is None:
        return ""
    if isinstance(valor, float) and valor.is_integer():
        valor = int(valor)
    return str(valor).strip()


def _sem_apostrofo(texto):
    """Desfaz o apóstrofo que a exportação põe antes de '=', '+', '-' e '@'."""
    if len(texto) > 1 and texto[0] == "'" and texto[1] in INICIOS_PERIGOSOS:
        return texto[1:]
    return texto


def _zero_vira_vazio(texto):
    """'0' e '0,00' querem dizer 'sem valor' para custo e multiplicador."""
    try:
        if Decimal(texto.replace(",", ".")) == 0:
            return ""
    except InvalidOperation:
        pass
    return texto


def _chave_do_nome(nome):
    """Para comparar nomes sem ligar para maiúsculas e espaços sobrando."""
    return " ".join(nome.split()).casefold()


def _conferir_zip(conteudo):
    """Um .xlsx é um zip: recusa macros e arquivos que 'incham' ao abrir."""
    try:
        with zipfile.ZipFile(io.BytesIO(conteudo)) as arquivo:
            itens = arquivo.infolist()
    except zipfile.BadZipFile:
        raise ErroDeImportacao(MENSAGEM_ABRIR) from None

    if any("vbaproject" in item.filename.lower() for item in itens):
        raise ErroDeImportacao(
            "Planilhas com macro não são aceitas. Salve como .xlsx comum."
        )

    if sum(item.file_size for item in itens) > LIMITE_DESCOMPACTADO:
        raise ErroDeImportacao("A planilha é grande demais para ser lida.")


def _linhas_xlsx(conteudo):
    """Primeira aba: lista de (número da linha, células)."""
    _conferir_zip(conteudo)

    try:
        pasta = load_workbook(io.BytesIO(conteudo), data_only=True)
        celulas = pasta.worksheets[0].iter_rows(
            max_row=LINHAS_DE_CABECALHO + LINHAS_MAXIMAS + 1,
            max_col=COLUNAS_MAXIMAS,
            values_only=True,
        )
        return list(enumerate(celulas, start=1))
      # O openpyxl levanta erros de tipos diferentes com arquivos estragados.
    # Para quem enviou, todos significam o mesmo: "não consegui abrir".
    except Exception:  # noqa: BLE001
        raise ErroDeImportacao(MENSAGEM_ABRIR) from None


def _decodificar(conteudo):
    for codificacao in ("utf-8-sig", "cp1252"):
        try:
            return conteudo.decode(codificacao)
        except UnicodeDecodeError:
            continue
    raise ErroDeImportacao("Não consegui ler os acentos do CSV. Salve como UTF-8.")


def _separador(texto):
    """';' (Excel brasileiro) ou ',', conforme a linha do cabeçalho."""
    linhas = texto.splitlines()[:LINHAS_DE_CABECALHO]
    cabecalho = next((li for li in linhas if "nome" in _normalizar(li)), "")
    return ";" if cabecalho.count(";") >= cabecalho.count(",") else ","


def _linhas_csv(conteudo):
    texto = _decodificar(conteudo)

    try:
        leitor = csv.reader(io.StringIO(texto), delimiter=_separador(texto))
        linhas = islice(leitor, LINHAS_DE_CABECALHO + LINHAS_MAXIMAS + 1)
        return list(enumerate(linhas, start=1))
    except csv.Error:
        raise ErroDeImportacao("Não consegui ler o CSV.") from None


def _achar_cabecalho(linhas):
    """Posição da linha de cabeçalho e o mapa campo -> número da coluna."""
    for posicao, (_, celulas) in enumerate(linhas[:LINHAS_DE_CABECALHO]):
        colunas = {
            _normalizar(valor): indice
            for indice, valor in enumerate(celulas)
            if valor is not None
        }
        if all(nome in colunas for nome in OBRIGATORIAS):
            return posicao, {c: i for c, i in colunas.items() if c in CAMPOS}

    raise ErroDeImportacao(
        "Não achei o cabeçalho. A planilha precisa ter as colunas Nome, "
        "Categoria, Estoque e Descrição, mais Preço (ou Custo e Multiplicador)."
    )


def _montar_formulario(celulas, colunas):
    """Uma linha da planilha vira um dicionário de textos, como o formulário."""
    form = {
        campo: _texto(celulas[indice]) if indice < len(celulas) else ""
        for campo, indice in colunas.items()
    }

    for campo in ("nome", "categoria", "descricao"):
        form[campo] = _sem_apostrofo(form[campo])

    for campo in ("custo", "multiplicador"):
        if campo in form:
            form[campo] = _zero_vira_vazio(form[campo])

    if "multiplicador" in form:
        form["multiplicador"] = form["multiplicador"].replace(",", ".")

    return form


def _produtos_das_linhas(linhas, nomes_existentes):
    posicao, colunas = _achar_cabecalho(linhas)

    com_dados = [
        (numero, celulas)
        for numero, celulas in linhas[posicao + 1:]
        if any(_texto(valor) for valor in celulas)
    ]
    if len(com_dados) > LINHAS_MAXIMAS:
        raise ErroDeImportacao(
            f"A planilha tem mais de {LINHAS_MAXIMAS} produtos. "
            "Divida em arquivos menores."
        )

    resultado = ResultadoImportacao()
    existentes = {_chave_do_nome(nome) for nome in nomes_existentes}
    vistos = set()

    for numero, celulas in com_dados:
        form = _montar_formulario(celulas, colunas)

        erro = validar_formulario(form)
        if erro:
            resultado.erros.append(f"Linha {numero}: {erro}")
            continue

        produto = campos_do_produto(form)
        nome = produto["nome"]
        chave = _chave_do_nome(nome)

        if chave in existentes:
            resultado.ignorados.append(
                f'Linha {numero}: "{nome}" já existe no sistema.'
            )
        elif chave in vistos:
            resultado.ignorados.append(
                f'Linha {numero}: "{nome}" aparece mais de uma vez na planilha.'
            )
        else:
            vistos.add(chave)
            resultado.produtos.append(produto)

    return resultado


def ler_produtos(nome_arquivo, conteudo, nomes_existentes=()):
    """Lê o arquivo enviado e devolve um ResultadoImportacao.

    Problemas do arquivo inteiro levantam ErroDeImportacao. Problemas de
    linhas ficam em resultado.erros, para a rota decidir (tudo ou nada).
    """
    if len(conteudo) > TAMANHO_MAXIMO:
        raise ErroDeImportacao("O arquivo é grande demais (máximo 2 MB).")

    nome = (nome_arquivo or "").lower()

    if nome.endswith(".xlsx"):
        linhas = _linhas_xlsx(conteudo)
    elif nome.endswith(".csv"):
        linhas = _linhas_csv(conteudo)
    else:
        raise ErroDeImportacao("Envie um arquivo .xlsx ou .csv.")

    return _produtos_das_linhas(linhas, nomes_existentes)
