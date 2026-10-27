"""O login e o logout vivem no blueprint 'auth', com as mesmas URLs de antes."""

from adonai.seguranca import ROTAS_PUBLICAS


def _endpoint_da_url(app, caminho):
    return next(
        regra.endpoint for regra in app.url_map.iter_rules()
        if regra.rule == caminho
    )


def test_login_e_logout_estao_no_blueprint_auth(client):
    app = client.application

    assert _endpoint_da_url(app, "/login") == "auth.login"
    assert _endpoint_da_url(app, "/logout") == "auth.logout"


def test_login_continua_sendo_pagina_publica():
    assert "auth.login" in ROTAS_PUBLICAS


def test_logout_volta_para_a_pagina_de_login(client):
    resposta = client.post("/logout")

    assert resposta.status_code == 302
    assert resposta.headers["Location"].endswith("/login")