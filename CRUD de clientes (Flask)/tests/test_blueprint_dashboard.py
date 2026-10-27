"""O painel vive no blueprint 'dashboard', com a mesma URL de antes."""


def test_rota_do_painel_esta_no_blueprint(client):
    por_url = {r.rule: r.endpoint for r in client.application.url_map.iter_rules()}

    assert por_url["/dashboard"] == "dashboard.dashboard"