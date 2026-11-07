"""Testes dos links de exportação na lista de produtos."""


def test_lista_mostra_os_links_de_exportacao(client):
    html = client.get("/produtos").get_data(as_text=True)

    assert 'href="/produtos/exportar/xlsx"' in html
    assert 'href="/produtos/exportar/csv"' in html


def test_links_levam_a_busca_junto(client):
    html = client.get("/produtos?q=anel").get_data(as_text=True)

    assert 'href="/produtos/exportar/xlsx?q=anel"' in html
    assert 'href="/produtos/exportar/csv?q=anel"' in html


def test_aviso_so_aparece_quando_ha_busca(client):
    sem_busca = client.get("/produtos").get_data(as_text=True)
    com_busca = client.get("/produtos?q=anel").get_data(as_text=True)

    assert "exportar-aviso" not in sem_busca
    assert "exportar-aviso" in com_busca
