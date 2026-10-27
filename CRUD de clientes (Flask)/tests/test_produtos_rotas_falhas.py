"""Se o banco falha, a foto recém-enviada não pode ficar sobrando no disco."""

import pytest

from ajudantes import (
    JPG,
    PNG,
    MULTIPART,
    _dados_foto,
    _arquivos_enviados,
    _criar_com_foto,
)


def _falha(*args, **kwargs):
    raise RuntimeError("banco indisponível")


def test_se_o_banco_falha_ao_cadastrar_a_foto_nova_e_apagada(
    client, produtos, monkeypatch
):
    monkeypatch.setattr("adonai.dados.produtos.criar", _falha)

    with pytest.raises(RuntimeError):
        client.post("/novo", data=_dados_foto(JPG), content_type=MULTIPART)

    assert _arquivos_enviados(client) == []


def test_se_o_banco_falha_ao_editar_a_foto_nova_e_apagada_e_a_antiga_fica(
    client, produtos, monkeypatch
):
    produto = _criar_com_foto(client, produtos)
    monkeypatch.setattr("adonai.dados.produtos.atualizar", _falha)

    with pytest.raises(RuntimeError):
        client.post(
            f"/editar/{produto['id']}",
            data=_dados_foto(PNG, "nova.png"),
            content_type=MULTIPART,
        )

    assert _arquivos_enviados(client) == [produto["foto"]]
    assert produtos.buscar_por_id(produto["id"])["foto"] == produto["foto"]