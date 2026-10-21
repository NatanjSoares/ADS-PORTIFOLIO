import re
import io
from pathlib import Path

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

def _entrar(cliente):
    with cliente.session_transaction() as sessao:
        sessao["usuario"] = "admin"


def test_post_sem_token_csrf_e_recusado(client_com_csrf, produtos):
    _entrar(client_com_csrf)
    resposta = client_com_csrf.post("/novo", data=_dados())
    assert resposta.status_code == 302
    assert produtos.buscar_por_nome("Anel") == []


def test_post_com_token_csrf_valido_funciona(client_com_csrf, produtos):
    _entrar(client_com_csrf)
    pagina = client_com_csrf.get("/novo").get_data(as_text=True)
    token = re.search(r'name="csrf_token" value="([^"]+)"', pagina).group(1)

    resposta = client_com_csrf.post("/novo", data=_dados(csrf_token=token))

    assert resposta.status_code == 302
    assert len(produtos.buscar_por_nome("Anel")) == 1


def test_login_exige_token_csrf(client_com_csrf):
    resposta = client_com_csrf.post(
        "/login", data={"usuario": "admin", "senha": "senha-de-teste"}
    )
    assert resposta.status_code == 302
    assert client_com_csrf.get("/produtos").status_code == 302  # continua sem entrar


def test_todo_formulario_post_tem_token_csrf():
    pasta = Path(__file__).parent.parent / "templates"
    padrao = re.compile(
        r'<form\b[^>]*\bmethod\s*=\s*"POST"[^>]*>(.*?)</form>', re.I | re.S
    )
    sem_token = []

    for arquivo in pasta.glob("*.html"):
        texto = arquivo.read_text(encoding="utf-8")
        for bloco in padrao.findall(texto):
            if "csrf_token" not in bloco:
                sem_token.append(arquivo.name)

    assert sem_token == []

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

JPG = b"\xff\xd8\xff\xe0" + b"\x00" * 100
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
MULTIPART = "multipart/form-data"


def _dados_foto(foto=None, nome_arquivo="foto.jpg", **extra):
    dados = _dados(**extra)
    if foto is not None:
        dados["foto"] = (io.BytesIO(foto), nome_arquivo)
    return dados


def _arquivos_enviados(cliente):
    pasta = cliente.application.config["UPLOAD_FOLDER"]
    return sorted(p.name for p in pasta.glob("*")) if pasta.exists() else []


# ---------- cadastro com foto ----------

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


# ---------- editar com foto ----------

def _criar_com_foto(client, produtos):
    client.post("/novo", data=_dados_foto(JPG), content_type=MULTIPART)
    return produtos.buscar_por_nome("Anel")[0]


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


# ---------- excluir com foto ----------

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
RAIZ = Path(__file__).parent.parent


def test_login_tem_a_hero_e_os_campos(client_anonimo):
    html = client_anonimo.get("/login").get_data(as_text=True)

    assert "login-imagem" in html
    assert "Área administrativa" in html
    assert 'name="usuario"' in html
    assert 'name="senha"' in html
    assert 'name="csrf_token"' in html


def test_lista_tem_a_janela_de_ampliacao(client):
    html = client.get("/produtos").get_data(as_text=True)

    assert 'id="foto-dialogo"' in html
    assert "js/ampliar.js" in html


def test_miniatura_com_foto_e_ampliavel(client, produtos):
    produtos.criar("Anel", "Joia", 10, 1, "x", foto="abc123.jpg")
    html = client.get("/produtos").get_data(as_text=True)

    assert 'data-grande="/static/uploads/abc123.jpg"' in html
    assert "foto-ampliavel" in html


def test_arquivos_citados_nos_templates_existem():
    padrao = re.compile(r"""filename\s*=\s*['"]([^'"]+)['"]""")
    faltando = []

    for template in (RAIZ / "templates").glob("*.html"):
        texto = template.read_text(encoding="utf-8")
        for nome in padrao.findall(texto):
            if nome.endswith("/"):
                continue  # pasta montada na hora (ex.: uploads/)
            if not (RAIZ / "static" / nome).exists():
                faltando.append(f"{template.name}: static/{nome}")

    assert faltando == []


def test_arquivos_citados_nos_css_existem():
    padrao = re.compile(r"""url\(\s*['"]?([^'")]+)['"]?\s*\)""")
    faltando = []

    for css in (RAIZ / "static" / "css").glob("*.css"):
        texto = css.read_text(encoding="utf-8")
        for caminho in padrao.findall(texto):
            if caminho.startswith(("http", "data:", "#")):
                continue
            if not (css.parent / caminho).resolve().exists():
                faltando.append(f"{css.name}: {caminho}")

    assert faltando == []


def test_main_css_importa_o_css_das_fotos():
    texto = (RAIZ / "static" / "css" / "main.css").read_text(encoding="utf-8")
    assert "foto.css" in texto    