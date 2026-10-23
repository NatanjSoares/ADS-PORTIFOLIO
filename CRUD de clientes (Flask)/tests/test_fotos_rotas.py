from ajudantes import (
    _dados,
    JPG,
    PNG,
    MULTIPART,
    _dados_foto,
    _arquivos_enviados,
    _criar_com_foto,
)


def test_cadastro_com_foto_valida(client, produtos):
    resposta = client.post("/novo", data=_dados_foto(JPG), content_type=MULTIPART)

    assert resposta.status_code == 302
    anel = produtos.buscar_por_nome("Anel")[0]
    assert anel["foto"].endswith(".jpg")
    assert _arquivos_enviados(client) == [anel["foto"]]


def test_cadastro_sem_foto_continua_funcionando(client, produtos):
    resposta = client.post("/novo", data=_dados())

    assert resposta.status_code == 302
    assert produtos.buscar_por_nome("Anel")[0]["foto"] is None
    assert _arquivos_enviados(client) == []


def test_foto_com_extensao_invalida_e_recusada(client, produtos):
    resposta = client.post(
        "/novo", data=_dados_foto(JPG, "documento.txt"), content_type=MULTIPART
    )

    assert resposta.status_code == 200
    assert "Formato inválido" in resposta.get_data(as_text=True)
    assert produtos.buscar_por_nome("Anel") == []
    assert _arquivos_enviados(client) == []


def test_arquivo_falso_com_nome_de_imagem_e_recusado(client, produtos):
    falso = b"<html><script>alert(1)</script></html>"
    resposta = client.post(
        "/novo", data=_dados_foto(falso, "foto.jpg"), content_type=MULTIPART
    )

    assert "não parece ser uma imagem" in resposta.get_data(as_text=True)
    assert produtos.buscar_por_nome("Anel") == []
    assert _arquivos_enviados(client) == []


def test_foto_acima_de_2mb_e_recusada(client, produtos):
    grande = JPG + b"\x00" * int(2.5 * 1024 * 1024)
    resposta = client.post(
        "/novo", data=_dados_foto(grande), content_type=MULTIPART
    )

    assert resposta.status_code == 200
    assert "2 MB" in resposta.get_data(as_text=True)
    assert produtos.buscar_por_nome("Anel") == []
    assert _arquivos_enviados(client) == []


def test_arquivo_acima_do_limite_geral_mostra_mensagem(client, produtos):
    enorme = JPG + b"\x00" * (4 * 1024 * 1024)
    resposta = client.post(
        "/novo",
        data=_dados_foto(enorme),
        content_type=MULTIPART,
        follow_redirects=True,
    )

    assert "2 MB" in resposta.get_data(as_text=True)
    assert produtos.buscar_por_nome("Anel") == []
    assert _arquivos_enviados(client) == []


def test_upload_sem_login_e_barrado(client_anonimo, produtos):
    resposta = client_anonimo.post(
        "/novo", data=_dados_foto(JPG), content_type=MULTIPART
    )

    assert resposta.status_code == 302
    assert "/login" in resposta.headers["Location"]
    assert produtos.buscar_por_nome("Anel") == []
    assert _arquivos_enviados(client_anonimo) == []


def test_erro_no_formulario_nao_salva_a_foto(client, produtos):
    resposta = client.post(
        "/novo", data=_dados_foto(JPG, nome=""), content_type=MULTIPART
    )

    assert "obrigatório" in resposta.get_data(as_text=True)
    assert _arquivos_enviados(client) == []


def test_editar_troca_a_foto_e_apaga_a_antiga(client, produtos):
    produto = _criar_com_foto(client, produtos)
    antiga = produto["foto"]

    resposta = client.post(
        f"/editar/{produto['id']}",
        data=_dados_foto(PNG, "nova.png"),
        content_type=MULTIPART,
    )

    assert resposta.status_code == 302
    nova = produtos.buscar_por_id(produto["id"])["foto"]
    assert nova != antiga and nova.endswith(".png")
    assert _arquivos_enviados(client) == [nova]


def test_editar_sem_nova_foto_mantem_a_atual(client, produtos):
    produto = _criar_com_foto(client, produtos)

    client.post(f"/editar/{produto['id']}", data=_dados(nome="Anel 2"))

    atual = produtos.buscar_por_id(produto["id"])
    assert atual["nome"] == "Anel 2"
    assert atual["foto"] == produto["foto"]
    assert _arquivos_enviados(client) == [produto["foto"]]


def test_editar_remove_a_foto_quando_pedido(client, produtos):
    produto = _criar_com_foto(client, produtos)

    client.post(
        f"/editar/{produto['id']}", data=_dados(remover_foto="1")
    )

    assert produtos.buscar_por_id(produto["id"])["foto"] is None
    assert _arquivos_enviados(client) == []


def test_editar_com_erro_nao_apaga_a_foto_antiga(client, produtos):
    produto = _criar_com_foto(client, produtos)

    resposta = client.post(
        f"/editar/{produto['id']}",
        data=_dados_foto(PNG, "nova.png", nome=""),
        content_type=MULTIPART,
    )

    assert resposta.status_code == 200
    assert produtos.buscar_por_id(produto["id"])["foto"] == produto["foto"]
    assert _arquivos_enviados(client) == [produto["foto"]]


def test_excluir_apaga_a_foto_do_disco(client, produtos):
    produto = _criar_com_foto(client, produtos)
    assert _arquivos_enviados(client) == [produto["foto"]]

    client.post(f"/excluir/{produto['id']}")

    assert produtos.buscar_por_id(produto["id"]) is None
    assert _arquivos_enviados(client) == []


def test_form_novo_aceita_envio_de_arquivo(client):
    html = client.get("/novo").get_data(as_text=True)

    assert 'enctype="multipart/form-data"' in html
    assert 'type="file"' in html
    assert 'name="foto"' in html
    assert 'name="remover_foto"' not in html


def test_editar_produto_com_foto_mostra_a_imagem_e_o_remover(client, produtos):
    novo = produtos.criar("Anel", "Joia", 10, 1, "x", foto="abc123.jpg")
    html = client.get(f"/editar/{novo['id']}").get_data(as_text=True)

    assert "/static/uploads/abc123.jpg" in html
    assert 'name="remover_foto"' in html


def test_editar_produto_sem_foto_nao_mostra_o_remover(client, produtos):
    novo = produtos.criar("Anel", "Joia", 10, 1, "x")
    html = client.get(f"/editar/{novo['id']}").get_data(as_text=True)

    assert 'name="remover_foto"' not in html
    assert "sem-foto.svg" not in html


def test_lista_mostra_a_foto_ou_a_imagem_padrao(client, produtos):
    produtos.criar("Com foto", "Joia", 10, 1, "x", foto="abc123.jpg")
    html = client.get("/produtos").get_data(as_text=True)

    sem_foto = len(produtos.listar_todos()) - 1  # todos, menos o que tem foto

    assert "/static/uploads/abc123.jpg" in html
    assert 'alt="Foto de Com foto"' in html
    assert html.count("sem-foto.svg") == sem_foto


def test_nome_com_html_aparece_escapado(client, produtos):
    produtos.criar("<script>alert(1)</script>", "Joia", 10, 1, "x",
                   foto="abc123.jpg")
    html = client.get("/produtos").get_data(as_text=True)

    assert "<script>alert(1)</script>" not in html
    assert "&lt;script&gt;" in html


def test_lista_tem_a_janela_de_ampliacao(client):
    html = client.get("/produtos").get_data(as_text=True)

    assert 'id="foto-dialogo"' in html
    assert "js/ampliar.js" in html


def test_miniatura_com_foto_e_ampliavel(client, produtos):
    produtos.criar("Anel", "Joia", 10, 1, "x", foto="abc123.jpg")
    html = client.get("/produtos").get_data(as_text=True)

    assert 'data-grande="/static/uploads/abc123.jpg"' in html
    assert "foto-ampliavel" in html
