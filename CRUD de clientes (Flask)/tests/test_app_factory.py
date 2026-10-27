"""Testes da fábrica create_app(): cada chamada devolve um app novo e completo."""

from pathlib import Path

import pytest

from adonai import create_app
from adonai.config import RAIZ
from adonai.dados import usuarios


@pytest.fixture
def ambiente(tmp_path, monkeypatch):
    """Variáveis de ambiente de teste (banco novo só deste teste)."""
    monkeypatch.setenv("DB_PATH", str(tmp_path / "fabrica.db"))
    monkeypatch.setenv("SECRET_KEY", "chave-de-teste")
    monkeypatch.setenv("ADMIN_USER", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "senha-de-teste")
    return tmp_path


def test_cada_chamada_devolve_um_app_novo(ambiente):
    primeiro = create_app()
    segundo = create_app()

    assert primeiro is not segundo


def test_templates_e_static_continuam_na_raiz(ambiente):
    app = create_app()

    assert Path(app.static_folder) == RAIZ / "static"
    assert Path(app.jinja_loader.searchpath[0]) == RAIZ / "templates"
    assert "static" in {regra.endpoint for regra in app.url_map.iter_rules()}


def test_config_extra_sobrescreve_a_padrao(ambiente):
    pasta = ambiente / "fotos"

    app = create_app({"TESTING": True, "UPLOAD_FOLDER": pasta})

    assert app.config["TESTING"] is True
    assert app.config["UPLOAD_FOLDER"] == pasta
    assert app.config["SECRET_KEY"] == "chave-de-teste"


def test_banco_e_usuario_admin_nascem_com_o_app(ambiente):
    app = create_app()

    assert (ambiente / "fabrica.db").exists()
    with app.app_context():
        assert usuarios.verificar_login("admin", "senha-de-teste")


def test_sem_secret_key_o_app_nao_sobe(ambiente, monkeypatch):
    monkeypatch.delenv("SECRET_KEY")

    with pytest.raises(RuntimeError):
        create_app()