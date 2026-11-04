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


def test_texto_dos_multiplicadores_cita_a_embalagem(client):
    html = client.get("/multiplicadores").get_data(as_text=True)

    assert "(custo + embalagem) × multiplicador" in html
