def test_home_abre(client):
    assert client.get("/").status_code == 200


def test_listar_abre(client):
    assert client.get("/produtos").status_code == 200


def test_cadastro_sem_nome_mostra_erro(client):
    resposta = client.post("/novo", data={
        "nome": "", "categoria": "Joia", "preco": "10",
        "estoque": "1", "descricao": "x",
    })
    assert "obrigatório" in resposta.get_data(as_text=True)


def test_cadastro_valido_redireciona(client):
    resposta = client.post("/novo", data={
        "nome": "Anel", "categoria": "Joia", "preco": "10",
        "estoque": "1", "descricao": "Tamanho 17",
    })
    assert resposta.status_code == 302


def test_preco_negativo_e_rejeitado(client):
    resposta = client.post("/novo", data={
        "nome": "Anel", "categoria": "Joia", "preco": "-5",
        "estoque": "1", "descricao": "x",
    })
    assert "negativo" in resposta.get_data(as_text=True)

def test_dashboard_abre(client):
    assert client.get("/dashboard").status_code == 200
def test_form_novo_lista_multiplicadores(client):
    html = client.get("/novo").get_data(as_text=True)
    assert "Básico" in html

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