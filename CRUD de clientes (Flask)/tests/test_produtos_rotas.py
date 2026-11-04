from ajudantes import (
    _dados,
)


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


def test_form_novo_lista_multiplicadores(client):
    html = client.get("/novo").get_data(as_text=True)
    assert "Básico" in html


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


def test_cadastro_com_embalagem_e_frete(client, produtos):
    from decimal import Decimal

    resposta = client.post("/novo", data=_dados(
        custo="20", multiplicador="2.5", embalagem="5", frete="12,90",
    ))

    assert resposta.status_code == 302
    criado = produtos.buscar_por_nome("Anel")[0]
    assert criado["preco"] == Decimal("62.50")       # (20 + 5) x 2,5
    assert criado["embalagem"] == Decimal("5.00")
    assert criado["frete"] == Decimal("12.90")


def test_embalagem_e_frete_sao_opcionais(client, produtos):
    from decimal import Decimal

    resposta = client.post("/novo", data=_dados())

    assert resposta.status_code == 302
    criado = produtos.buscar_por_nome("Anel")[0]
    assert criado["embalagem"] == Decimal("0.00")
    assert criado["frete"] == Decimal("0.00")


def test_embalagem_negativa_e_recusada(client, produtos):
    resposta = client.post("/novo", data=_dados(embalagem="-1"))

    assert "A embalagem não pode ser negativa" in resposta.get_data(as_text=True)
    assert produtos.buscar_por_nome("Anel") == []


def test_frete_invalido_e_recusado(client, produtos):
    resposta = client.post("/novo", data=_dados(frete="abc"))

    assert "valor válido para o frete" in resposta.get_data(as_text=True)
    assert produtos.buscar_por_nome("Anel") == []


def test_frete_negativo_e_recusado(client, produtos):
    resposta = client.post("/novo", data=_dados(frete="-5"))

    assert "O frete não pode ser negativo" in resposta.get_data(as_text=True)
    assert produtos.buscar_por_nome("Anel") == []


def test_editar_salva_embalagem_e_frete(client, produtos):
    from decimal import Decimal

    produto = produtos.criar("Brinco", "Joia", 0, 1, "x",
                             custo=20, multiplicador=2.5)

    resposta = client.post(f"/editar/{produto['id']}", data=_dados(
        nome="Brinco", custo="20", multiplicador="2.5",
        embalagem="5", frete="8",
    ))

    assert resposta.status_code == 302
    atual = produtos.buscar_por_id(produto["id"])
    assert atual["preco"] == Decimal("62.50")
    assert atual["frete"] == Decimal("8.00")


def test_formulario_tem_embalagem_e_frete(client):
    html = client.get("/novo").get_data(as_text=True)

    assert 'id="embalagem"' in html
    assert 'name="embalagem"' in html
    assert 'id="frete"' in html
    assert 'name="frete"' in html


def test_campos_do_formulario_na_ordem_combinada(client):
    html = client.get("/novo").get_data(as_text=True)

    ordem = ['id="custo"', 'id="embalagem"', 'id="frete"',
             'id="multiplicador"', 'id="preco"']
    posicoes = [html.index(item) for item in ordem]

    assert posicoes == sorted(posicoes)


def test_editar_mostra_embalagem_e_frete_salvos(client, produtos):
    produto = produtos.criar("Anel", "Joia", 0, 1, "x",
                             custo=20, multiplicador=2.5,
                             embalagem=5, frete=12.9)

    html = client.get(f"/editar/{produto['id']}").get_data(as_text=True)

    assert 'value="5.00"' in html
    assert 'value="12.90"' in html


def test_formulario_com_erro_mantem_embalagem_e_frete_digitados(client):
    resposta = client.post("/novo", data=_dados(
        nome="", embalagem="3.5", frete="9",
    ))

    html = resposta.get_data(as_text=True)
    assert 'value="3.5"' in html
    assert 'value="9"' in html


def test_lista_mostra_o_custo_com_embalagem(client, produtos):
    produtos.criar("Anel", "Joia", 0, 1, "x",
                   custo=20, multiplicador=2.5, embalagem=5)

    html = client.get("/produtos").get_data(as_text=True)

    assert "R$ 25.00" in html
    assert 'title="Custo R$ 20.00 + embalagem R$ 5.00"' in html


def test_celulas_de_valor_nao_quebram_linha(client):
    html = client.get("/produtos").get_data(as_text=True)

    assert 'class="valor"' in html
