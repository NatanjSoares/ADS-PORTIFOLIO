from datetime import timedelta

import pytest

from adonai.config import RAIZ, carregar_config
from adonai.seguranca import ROTAS_PUBLICAS


def test_sem_secret_key_a_configuracao_nao_carrega(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)

    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        carregar_config()


def test_valores_padrao_da_configuracao(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "chave")
    monkeypatch.delenv("COOKIE_SEGURO", raising=False)
    monkeypatch.delenv("UPLOAD_DIR", raising=False)

    config = carregar_config()

    assert config["SECRET_KEY"] == "chave"
    assert config["SESSION_COOKIE_HTTPONLY"] is True
    assert config["SESSION_COOKIE_SAMESITE"] == "Lax"
    assert config["SESSION_COOKIE_SECURE"] is False
    assert config["PERMANENT_SESSION_LIFETIME"] == timedelta(hours=8)
    assert config["WTF_CSRF_TIME_LIMIT"] is None
    assert config["MAX_CONTENT_LENGTH"] == 3 * 1024 * 1024
    assert config["UPLOAD_FOLDER"] == RAIZ / "static" / "uploads"


def test_cookie_seguro_liga_com_a_variavel(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "chave")
    monkeypatch.setenv("COOKIE_SEGURO", "1")

    assert carregar_config()["SESSION_COOKIE_SECURE"] is True


def test_pasta_das_fotos_pode_ser_trocada_pela_variavel(monkeypatch, tmp_path):
    monkeypatch.setenv("SECRET_KEY", "chave")
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "fotos"))

    assert carregar_config()["UPLOAD_FOLDER"] == tmp_path / "fotos"


def test_raiz_do_projeto_esta_certa():
    assert (RAIZ / "adonai").is_dir()
    assert (RAIZ / "templates").is_dir()


def test_app_usa_a_configuracao_carregada(client):
    app = client.application

    assert app.config["SESSION_COOKIE_SAMESITE"] == "Lax"
    assert app.config["SESSION_COOKIE_HTTPONLY"] is True
    assert app.config["MAX_CONTENT_LENGTH"] == 3 * 1024 * 1024
    assert app.secret_key


def test_extensoes_estao_ligadas_ao_app(client):
    assert "csrf" in client.application.extensions
    assert "limiter" in client.application.extensions


def test_so_o_login_e_os_arquivos_estaticos_sao_publicos():
    assert ROTAS_PUBLICAS == {"login", "static"}