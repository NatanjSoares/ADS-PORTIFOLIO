import re
from pathlib import Path

from ajudantes import (
    _dados,
    _entrar,
)


def test_post_sem_token_csrf_e_recusado(client_com_csrf, produtos):
    _entrar(client_com_csrf)
    resposta = client_com_csrf.post("/novo", data=_dados())
    assert resposta.status_code == 302
    assert produtos.buscar_por_nome("Anel") == []


def test_post_com_token_csrf_valido_funciona(client_com_csrf, produtos):
    _entrar(client_com_csrf)
    pagina = client_com_csrf.get("/novo").get_data(as_text=True)
    token = re.search(r'name="csrf_token" value="([^"]+)"', pagina).group(1)

    resposta = client_com_csrf.post("/novo", data=_dados(csrf_token=token))

    assert resposta.status_code == 302
    assert len(produtos.buscar_por_nome("Anel")) == 1


def test_todo_formulario_post_tem_token_csrf():
    pasta = Path(__file__).parent.parent / "templates"
    padrao = re.compile(
        r'<form\b[^>]*\bmethod\s*=\s*"POST"[^>]*>(.*?)</form>', re.I | re.S
    )
    sem_token = []

    for arquivo in pasta.glob("*.html"):
        texto = arquivo.read_text(encoding="utf-8")
        for bloco in padrao.findall(texto):
            if "csrf_token" not in bloco:
                sem_token.append(arquivo.name)

    assert sem_token == []
