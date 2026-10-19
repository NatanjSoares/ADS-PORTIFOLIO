import io

import pytest
from werkzeug.datastructures import FileStorage

import fotos

# Cabeçalhos mínimos de cada formato (o que o validador confere)
JPG = b"\xff\xd8\xff\xe0" + b"\x00" * 100
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100
WEBP = b"RIFF\x00\x00\x00\x00WEBP" + b"\x00" * 100


def arquivo(conteudo, nome):
    return FileStorage(stream=io.BytesIO(conteudo), filename=nome)


@pytest.mark.parametrize("nome, conteudo", [
    ("foto.jpg", JPG),
    ("foto.png", PNG),
    ("foto.webp", WEBP),
    ("FOTO.JPEG", JPG),
])
def test_foto_valida_e_aceita(nome, conteudo):
    assert fotos.validar_foto(arquivo(conteudo, nome)) is None


def test_sem_arquivo_nao_e_erro():
    assert fotos.validar_foto(None) is None
    assert fotos.validar_foto(arquivo(b"", "")) is None


@pytest.mark.parametrize("nome", ["doc.txt", "script.exe", "foto", "foto.gif"])
def test_extensao_invalida_e_recusada(nome):
    assert "Formato inválido" in fotos.validar_foto(arquivo(JPG, nome))


def test_arquivo_falso_com_extensao_de_imagem():
    falso = arquivo(b"<html><script>alert(1)</script></html>", "foto.jpg")
    assert "não parece ser uma imagem" in fotos.validar_foto(falso)


def test_extensao_nao_combina_com_conteudo():
    assert "não combina" in fotos.validar_foto(arquivo(PNG, "foto.jpg"))


def test_arquivo_vazio_e_recusado():
    assert "vazio" in fotos.validar_foto(arquivo(b"", "foto.jpg"))


def test_arquivo_grande_e_recusado():
    grande = JPG + b"\x00" * fotos.TAMANHO_MAX
    assert "2 MB" in fotos.validar_foto(arquivo(grande, "foto.jpg"))


def test_arquivo_no_limite_e_aceito():
    no_limite = JPG + b"\x00" * (fotos.TAMANHO_MAX - len(JPG))
    assert len(no_limite) == fotos.TAMANHO_MAX
    assert fotos.validar_foto(arquivo(no_limite, "foto.jpg")) is None


def test_nome_com_acento_e_aceito():
    assert fotos.validar_foto(arquivo(JPG, "ação.jpg")) is None


def test_salvar_gera_nome_aleatorio_e_grava(tmp_path):
    pasta = tmp_path / "uploads"
    nome1 = fotos.salvar_foto(arquivo(JPG, "foto.jpg"), pasta)
    nome2 = fotos.salvar_foto(arquivo(JPG, "foto.jpg"), pasta)

    assert nome1 != nome2
    assert nome1 != "foto.jpg"
    assert nome1.endswith(".jpg")
    assert (pasta / nome1).read_bytes() == JPG


def test_nome_malicioso_nao_sai_da_pasta(tmp_path):
    pasta = tmp_path / "uploads"
    nome = fotos.salvar_foto(arquivo(JPG, "../../fuga.jpg"), pasta)

    assert "/" not in nome and "\\" not in nome
    assert (pasta / nome).exists()
    assert not (tmp_path / "fuga.jpg").exists()


def test_remover_foto_apaga_o_arquivo(tmp_path):
    pasta = tmp_path / "uploads"
    nome = fotos.salvar_foto(arquivo(PNG, "foto.png"), pasta)

    assert fotos.remover_foto(nome, pasta) is True
    assert not (pasta / nome).exists()


def test_remover_foto_inexistente_nao_da_erro(tmp_path):
    assert fotos.remover_foto("nao-existe.jpg", tmp_path) is False
    assert fotos.remover_foto(None, tmp_path) is False


def test_remover_nao_sai_da_pasta(tmp_path):
    pasta = tmp_path / "uploads"
    pasta.mkdir()
    segredo = tmp_path / "segredo.txt"
    segredo.write_text("não apague")

    assert fotos.remover_foto("../segredo.txt", pasta) is False
    assert segredo.exists()