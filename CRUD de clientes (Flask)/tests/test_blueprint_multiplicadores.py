"""Multiplicadores vivem no blueprint 'multiplicadores', com as mesmas URLs."""

import pytest
from flask import template_rendered

ROTAS = {
    "/multiplicadores": "multiplicadores.multiplicadores_view",
    "/multiplicadores/<int:mult_id>/excluir": "multiplicadores.excluir_multiplicador",
}


@pytest.mark.parametrize("url, endpoint", ROTAS.items())
def test_rota_de_multiplicadores_esta_no_blueprint(client, url, endpoint):
    por_url = {r.rule: r.endpoint for r in client.application.url_map.iter_rules()}

    assert por_url[url] == endpoint


def test_lista_de_multiplicadores_chega_em_paginas_de_outros_blueprints(client):
    """O context_processor vale para o app inteiro, não só para esta gaveta."""
    contextos = []

    def gravar(sender, template, context, **extra):
        contextos.append(context)

    template_rendered.connect(gravar, client.application)
    try:
        client.get("/produtos")
    finally:
        template_rendered.disconnect(gravar, client.application)

    assert contextos
    assert "multiplicadores" in contextos[0]