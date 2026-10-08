import importlib

import pytest


@pytest.fixture
def produtos(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "teste.db"))
    import produtos as modulo
    importlib.reload(modulo)
    return modulo


@pytest.fixture
def client(produtos, monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "chave-de-teste")
    import app as modulo_app
    modulo_app.app.config["TESTING"] = True
    return modulo_app.app.test_client()