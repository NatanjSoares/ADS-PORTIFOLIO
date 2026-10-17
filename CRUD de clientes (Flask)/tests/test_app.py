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


# ---------- editar ----------

def test_editar_mostra_dados_do_produto(client, produtos):
    novo = produtos.criar("Brinco de prata", "Joia", 50.0, 3, "Pequeno")
    resposta = client.get(f"/editar/{novo['id']}")
    assert resposta.status_code == 200
    assert "Brinco de prata" in resposta.get_data(as_text=True)


def test_editar_salva_alteracoes(client, produtos):
    novo = produtos.criar("Brinco", "Joia", 50.0, 3, "Pequeno")
    resposta = client.post(
        f"/editar/{novo['id']}",
        data=_dados(nome="Brinco grande", preco="60", estoque="2"),
    )
    assert resposta.status_code == 302
    salvo = produtos.buscar_por_id(novo["id"])
    assert salvo["nome"] == "Brinco grande"
    assert salvo["preco"] == 60.0
    assert salvo["estoque"] == 2


def test_editar_com_erro_nao_altera_o_produto(client, produtos):
    novo = produtos.criar("Brinco", "Joia", 50.0, 3, "Pequeno")
    resposta = client.post(f"/editar/{novo['id']}", data=_dados(nome=""))
    assert resposta.status_code == 200
    assert "obrigatório" in resposta.get_data(as_text=True)
    assert produtos.buscar_por_id(novo["id"])["nome"] == "Brinco"


def test_editar_produto_inexistente_redireciona(client):
    resposta = client.get("/editar/99999")
    assert resposta.status_code == 302


# ---------- excluir ----------

def test_excluir_remove_o_produto(client, produtos):
    novo = produtos.criar("Pulseira", "Joia", 40.0, 4, "Fina")
    resposta = client.post(f"/excluir/{novo['id']}")
    assert resposta.status_code == 302
    assert produtos.buscar_por_id(novo["id"]) is None


def test_excluir_inexistente_mostra_aviso(client):
    resposta = client.post("/excluir/99999", follow_redirects=True)
    assert "não encontrado" in resposta.get_data(as_text=True)


def test_excluir_nao_aceita_get(client, produtos):
    novo = produtos.criar("Pulseira", "Joia", 40.0, 4, "Fina")
    resposta = client.get(f"/excluir/{novo['id']}")
    assert resposta.status_code == 405
    assert produtos.buscar_por_id(novo["id"]) is not None


# ---------- multiplicador no cadastro ----------

def test_cadastro_calcula_preco_pelo_multiplicador(client, produtos):
    resposta = client.post("/novo", data={
        "nome": "Anel com multiplicador",
        "categoria": "Joia",
        "custo": "20",
        "multiplicador": "2.5",
        "estoque": "1",
        "descricao": "x",
    })
    assert resposta.status_code == 302
    criado = produtos.buscar_por_nome("Anel com multiplicador")[0]
    assert criado["preco"] == 50.0
    assert criado["custo"] == 20.0


# ---------- tela de multiplicadores ----------

def test_multiplicadores_lista_os_cadastrados(client):
    resposta = client.get("/multiplicadores")
    assert resposta.status_code == 200
    assert "Básico" in resposta.get_data(as_text=True)


def test_criar_multiplicador(client, produtos):
    resposta = client.post("/multiplicadores", data={"nome": "Especial", "valor": "3.2"})
    assert resposta.status_code == 302
    nomes = [m["nome"] for m in produtos.listar_multiplicadores()]
    assert "Especial" in nomes


def test_multiplicador_fora_da_faixa_nao_e_salvo(client, produtos):
    antes = len(produtos.listar_multiplicadores())
    resposta = client.post(
        "/multiplicadores",
        data={"nome": "Alto demais", "valor": "5"},
        follow_redirects=True,
    )
    assert "entre 1,5 e 4" in resposta.get_data(as_text=True)
    assert len(produtos.listar_multiplicadores()) == antes


def test_multiplicador_sem_nome_nao_e_salvo(client, produtos):
    antes = len(produtos.listar_multiplicadores())
    resposta = client.post(
        "/multiplicadores",
        data={"nome": "", "valor": "2"},
        follow_redirects=True,
    )
    assert "obrigatório" in resposta.get_data(as_text=True)
    assert len(produtos.listar_multiplicadores()) == antes


def test_atualizar_multiplicador(client, produtos):
    primeiro = produtos.listar_multiplicadores()[0]
    client.post("/multiplicadores", data={
        "id": primeiro["id"], "nome": "Renomeado", "valor": "2.5",
    })
    nomes = [m["nome"] for m in produtos.listar_multiplicadores()]
    assert "Renomeado" in nomes


def test_excluir_multiplicador(client, produtos):
    primeiro = produtos.listar_multiplicadores()[0]
    resposta = client.post(f"/multiplicadores/{primeiro['id']}/excluir")
    assert resposta.status_code == 302
    ids = [m["id"] for m in produtos.listar_multiplicadores()]
    assert primeiro["id"] not in ids    