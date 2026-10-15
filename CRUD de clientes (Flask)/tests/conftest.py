import importlib

import pytest


@pytest.fixture
def produtos(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "teste.db"))
    import produtos as modulo
    importlib.reload(modulo)
    return modulo


@pytest.fixture
def client_anonimo(produtos, monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "chave-de-teste")
    monkeypatch.setenv("ADMIN_USER", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "senha-de-teste")

    import usuarios
    import app as modulo_app

    usuarios.inicializar_usuarios()
    modulo_app.app.config["TESTING"] = True
    return modulo_app.app.test_client()


@pytest.fixture
def client(client_anonimo):
    with client_anonimo.session_transaction() as sessao:
        sessao["usuario"] = "admin"
    return client_anonimo