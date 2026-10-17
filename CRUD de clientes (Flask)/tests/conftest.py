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
    modulo_app.app.config["WTF_CSRF_ENABLED"] = False
    modulo_app.limiter.enabled = False
    return modulo_app.app.test_client()


@pytest.fixture
def client(client_anonimo):
    with client_anonimo.session_transaction() as sessao:
        sessao["usuario"] = "admin"
    return client_anonimo


@pytest.fixture
def client_com_csrf(client_anonimo):
    import app as modulo_app

    modulo_app.app.config["WTF_CSRF_ENABLED"] = True
    yield client_anonimo
    modulo_app.app.config["WTF_CSRF_ENABLED"] = False


@pytest.fixture
def client_com_limite(client_anonimo):
    import app as modulo_app

    modulo_app.limiter.reset()
    modulo_app.limiter.enabled = True
    yield client_anonimo
    modulo_app.limiter.enabled = False
    modulo_app.limiter.reset()