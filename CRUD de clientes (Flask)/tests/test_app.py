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