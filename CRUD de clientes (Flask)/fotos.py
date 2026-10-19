"""Regras das fotos dos produtos: validar, salvar e apagar."""

import os
import uuid
from pathlib import Path

from werkzeug.utils import secure_filename

EXTENSOES = {"jpg", "jpeg", "png", "webp"}
TAMANHO_MAX = 2 * 1024 * 1024  # 2 MB


def tem_foto(arquivo):
    """True se o formulário trouxe um arquivo escolhido."""
    return bool(arquivo and arquivo.filename)


def _extensao(nome):
    """Extensão do nome original, em minúsculas e sem o ponto."""
    sufixo = Path(nome or "").suffix.lower().lstrip(".")
    return secure_filename(sufixo)


def _tipo_pelo_conteudo(inicio):
    """Descobre o formato olhando os primeiros bytes do arquivo."""
    if inicio.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if inicio.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if inicio[:4] == b"RIFF" and inicio[8:12] == b"WEBP":
        return "webp"
    return None


def _ler_inicio(arquivo):
    arquivo.stream.seek(0)
    inicio = arquivo.stream.read(12)
    arquivo.stream.seek(0)
    return inicio


def _tamanho(arquivo):
    arquivo.stream.seek(0, os.SEEK_END)
    tamanho = arquivo.stream.tell()
    arquivo.stream.seek(0)
    return tamanho


def validar_foto(arquivo):
    """Devolve uma mensagem de erro, ou None se a foto está ok (ou ausente)."""
    if not tem_foto(arquivo):
        return None

    extensao = _extensao(arquivo.filename)
    if extensao not in EXTENSOES:
        return "Formato inválido. Use JPG, PNG ou WEBP."

    tamanho = _tamanho(arquivo)
    if tamanho == 0:
        return "O arquivo da foto está vazio."
    if tamanho > TAMANHO_MAX:
        return "A foto deve ter no máximo 2 MB."

    tipo = _tipo_pelo_conteudo(_ler_inicio(arquivo))
    if tipo is None:
        return "O arquivo não parece ser uma imagem válida."

    esperado = "jpg" if extensao == "jpeg" else extensao
    if tipo != esperado:
        return "A extensão do arquivo não combina com o seu conteúdo."

    return None


def salvar_foto(arquivo, pasta):
    """Grava a foto com nome aleatório e devolve só o nome do arquivo."""
    tipo = _tipo_pelo_conteudo(_ler_inicio(arquivo))
    if tipo is None:
        raise ValueError("Arquivo não é uma imagem válida.")

    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)

    nome = f"{uuid.uuid4().hex}.{tipo}"
    arquivo.save(pasta / nome)
    return nome


def remover_foto(nome, pasta):
    """Apaga a foto da pasta. Devolve True se apagou."""
    if not nome:
        return False

    pasta = Path(pasta).resolve()
    alvo = (pasta / nome).resolve()

    if alvo.parent != pasta:
        return False  # nome estranho (ex.: ../): não apaga nada

    try:
        alvo.unlink()
    except FileNotFoundError:
        return False
    return True