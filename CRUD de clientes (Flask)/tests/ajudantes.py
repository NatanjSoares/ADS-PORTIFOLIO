"""Funções e constantes usadas por vários arquivos de teste."""

import io
from pathlib import Path


def _dados(**extra):
    dados = {
        "nome": "Anel",
        "categoria": "Joia",
        "preco": "10",
        "estoque": "1",
        "descricao": "x",
    }
    dados.update(extra)
    return dados


def _entrar(cliente):
    with cliente.session_transaction() as sessao:
        sessao["usuario"] = "admin"


JPG = b"\xff\xd8\xff\xe0" + b"\x00" * 100


PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100


MULTIPART = "multipart/form-data"


def _dados_foto(foto=None, nome_arquivo="foto.jpg", **extra):
    dados = _dados(**extra)
    if foto is not None:
        dados["foto"] = (io.BytesIO(foto), nome_arquivo)
    return dados


def _arquivos_enviados(cliente):
    pasta = cliente.application.config["UPLOAD_FOLDER"]
    return sorted(p.name for p in pasta.glob("*")) if pasta.exists() else []


def _criar_com_foto(client, produtos):
    client.post("/novo", data=_dados_foto(JPG), content_type=MULTIPART)
    return produtos.buscar_por_nome("Anel")[0]


RAIZ = Path(__file__).parent.parent
