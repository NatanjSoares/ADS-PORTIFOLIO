"""Ponto de entrada: o wsgi.py cria o app e o app.py antigo não existe mais."""

from flask import Flask

from adonai.config import RAIZ


def test_wsgi_expoe_um_app_flask(tmp_path, monkeypatch):
    monkeypatch.setenv("DB_PATH", str(tmp_path / "wsgi.db"))
    monkeypatch.setenv("SECRET_KEY", "chave-de-teste")
    monkeypatch.setenv("ADMIN_USER", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "senha-de-teste")

    import wsgi

    assert isinstance(wsgi.app, Flask)


def test_app_py_antigo_foi_removido():
    assert not (RAIZ / "app.py").exists()


def test_dockerfile_inicia_pelo_wsgi():
    texto = (RAIZ / "Dockerfile").read_text(encoding="utf-8")

    assert "wsgi:app" in texto
    assert "app:app" not in texto.replace("wsgi:app", "")