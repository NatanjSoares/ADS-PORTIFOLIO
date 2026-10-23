import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).parent.parent
PAGINAS = ["/", "/produtos", "/novo", "/multiplicadores", "/dashboard"]


def _endpoints_citados():
    """Nomes usados em url_for(...) nos templates e no código Python."""
    padrao = re.compile(r"""url_for\(\s*['"]([^'"]+)['"]""")
    fontes = list((RAIZ / "templates").glob("*.html"))
    fontes.append(RAIZ / "app.py")
    if (RAIZ / "adonai").exists():
        fontes += list((RAIZ / "adonai").rglob("*.py"))

    achados = {}
    for arquivo in fontes:
        if not arquivo.exists():
            continue
        texto = arquivo.read_text(encoding="utf-8")
        for nome in padrao.findall(texto):
            achados.setdefault(nome, set()).add(arquivo.name)
    return achados


def test_todo_url_for_aponta_para_uma_rota_que_existe(client):
    existentes = {r.endpoint for r in client.application.url_map.iter_rules()}

    faltando = {
        nome: sorted(onde)
        for nome, onde in _endpoints_citados().items()
        if nome not in existentes
    }

    assert faltando == {}


@pytest.mark.parametrize("caminho", PAGINAS)
def test_pagina_abre_para_quem_esta_logado(client, caminho):
    assert client.get(caminho).status_code == 200


@pytest.mark.parametrize("caminho", PAGINAS)
def test_pagina_exige_login(client_anonimo, caminho):
    resposta = client_anonimo.get(caminho)

    assert resposta.status_code == 302
    assert "/login" in resposta.headers["Location"]


def test_pagina_de_login_abre_sem_estar_logado(client_anonimo):
    assert client_anonimo.get("/login").status_code == 200


def test_pagina_de_edicao_abre(client, produtos):
    produto = produtos.criar("Anel", "Joia", 10, 1, "x")

    assert client.get(f"/editar/{produto['id']}").status_code == 200