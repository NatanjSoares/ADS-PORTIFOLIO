def test_sem_login_redireciona_para_login(client_anonimo):
    resposta = client_anonimo.get("/produtos")
    assert resposta.status_code == 302
    assert "/login" in resposta.headers["Location"]


def test_login_correto_libera_acesso(client_anonimo):
    resposta = client_anonimo.post(
        "/login", data={"usuario": "admin", "senha": "senha-de-teste"}
    )
    assert resposta.status_code == 302
    assert client_anonimo.get("/produtos").status_code == 200


def test_login_com_senha_errada_e_recusado(client_anonimo):
    resposta = client_anonimo.post(
        "/login", data={"usuario": "admin", "senha": "errada"}
    )
    assert "inválidos" in resposta.get_data(as_text=True)
    assert client_anonimo.get("/produtos").status_code == 302


def test_logout_encerra_a_sessao(client):
    client.post("/logout")
    assert client.get("/produtos").status_code == 302


def test_senha_e_guardada_com_hash(client_anonimo, produtos):
    from contextlib import closing

    with closing(produtos._conectar()) as conexao:
        senha_hash = conexao.execute(
            "SELECT senha_hash FROM usuarios"
        ).fetchone()["senha_hash"]
    assert "senha-de-teste" not in senha_hash


def test_login_exige_token_csrf(client_com_csrf):
    resposta = client_com_csrf.post(
        "/login", data={"usuario": "admin", "senha": "senha-de-teste"}
    )
    assert resposta.status_code == 302
    assert client_com_csrf.get("/produtos").status_code == 302  # continua sem entrar


def test_login_bloqueia_apos_varias_tentativas(client_com_limite):
    for _ in range(5):
        resposta = client_com_limite.post(
            "/login", data={"usuario": "admin", "senha": "errada"}
        )
        assert resposta.status_code == 200

    resposta = client_com_limite.post(
        "/login", data={"usuario": "admin", "senha": "errada"}
    )
    assert resposta.status_code == 429
    assert "Muitas tentativas" in resposta.get_data(as_text=True)


def test_abrir_a_pagina_de_login_nao_conta_no_limite(client_com_limite):
    for _ in range(10):
        assert client_com_limite.get("/login").status_code == 200


def test_login_tem_a_hero_e_os_campos(client_anonimo):
    html = client_anonimo.get("/login").get_data(as_text=True)

    assert "login-imagem" in html
    assert "Área administrativa" in html
    assert 'name="usuario"' in html
    assert 'name="senha"' in html
    assert 'name="csrf_token"' in html
