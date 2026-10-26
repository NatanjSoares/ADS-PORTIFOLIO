import pytest
from flask import Flask

from adonai.dados import banco
from adonai.dados import produtos as dados_produtos


def _app_com_banco(caminho):
    app = Flask("teste")
    app.config["DB_PATH"] = caminho
    return app


def test_cada_app_tem_o_seu_proprio_banco(tmp_path):
    app_a = _app_com_banco(tmp_path / "a.db")
    app_b = _app_com_banco(tmp_path / "b.db")

    with app_a.app_context():
        banco.inicializar_banco()
        dados_produtos.criar("Só no A", "Joia", 10, 1, "x")
        total_a = len(dados_produtos.listar_todos())

    with app_b.app_context():
        banco.inicializar_banco()
        total_b = len(dados_produtos.listar_todos())

    assert total_a == 3  # os 2 de exemplo + o novo
    assert total_b == 2  # o banco do B não recebeu nada do A


def test_sem_app_ativo_nao_existe_banco():
    with pytest.raises(RuntimeError):
        banco.conectar()


def test_inicializar_banco_cria_a_pasta_que_nao_existe(tmp_path):
    caminho = tmp_path / "pasta" / "nova" / "teste.db"

    with _app_com_banco(caminho).app_context():
        banco.inicializar_banco()

    assert caminho.exists()