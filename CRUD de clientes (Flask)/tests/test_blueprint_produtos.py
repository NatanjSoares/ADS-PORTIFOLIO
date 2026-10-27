"""As rotas de produtos vivem no blueprint 'produtos', com as mesmas URLs."""

import pytest

ROTAS = {
    "/": "produtos.home",
    "/produtos": "produtos.listar",
    "/novo": "produtos.novo",
    "/editar/<int:produto_id>": "produtos.editar",
    "/excluir/<int:produto_id>": "produtos.excluir",
}


@pytest.mark.parametrize("url, endpoint", ROTAS.items())
def test_rota_de_produtos_esta_no_blueprint(client, url, endpoint):
    por_url = {r.rule: r.endpoint for r in client.application.url_map.iter_rules()}

    assert por_url[url] == endpoint