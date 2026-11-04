def test_dashboard_abre(client):
    assert client.get("/dashboard").status_code == 200


def test_dashboard_margem_desconta_a_embalagem(client, produtos):
    # preço = (20 + 5) x 2,5 = 62,50; custo total = 25 -> margem de 60%
    produtos.criar("Anel", "Joia", 0, 1, "x",
                   custo=20, multiplicador=2.5, embalagem=5)

    html = client.get("/dashboard").get_data(as_text=True)

    assert "60.0%" in html
    assert "68.0%" not in html   # seria a margem sem descontar a embalagem


def test_grafico_do_dashboard_usa_o_custo_com_embalagem(client, produtos):
    produtos.criar("Anel", "Joia", 0, 1, "x",
                   custo=20, multiplicador=2.5, embalagem=5)

    html = client.get("/dashboard").get_data(as_text=True)

    assert '"custos": [25.0]' in html


def test_dashboard_tem_uma_caixa_para_cada_grafico(client):
    html = client.get("/dashboard").get_data(as_text=True)

    assert html.count('class="grafico-caixa"') == 3
