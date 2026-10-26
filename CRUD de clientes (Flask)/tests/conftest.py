from contextlib import contextmanager
from types import SimpleNamespace

import pytest

from adonai.dados import banco, multiplicadores, usuarios
from adonai.dados import produtos as dados_produtos
from adonai.regras import dinheiro


def _dados():
    """Reúne as funções de dados num só objeto, como o antigo produtos.py."""
    return SimpleNamespace(
        listar_todos=dados_produtos.listar_todos,
        buscar_por_id=dados_produtos.buscar_por_id,
        buscar_por_nome=dados_produtos.buscar_por_nome,
        criar=dados_produtos.criar,
        atualizar=dados_produtos.atualizar,
        definir_foto=dados_produtos.definir_foto,
        excluir=dados_produtos.excluir,
        listar_multiplicadores=multiplicadores.listar_multiplicadores,
        criar_multiplicador=multiplicadores.criar_multiplicador,
        atualizar_multiplicador=multiplicadores.atualizar_multiplicador,
        excluir_multiplicador=multiplicadores.excluir_multiplicador,
        MULT_MIN=dinheiro.MULT_MIN,
        MULT_MAX=dinheiro.MULT_MAX,
        _conectar=banco.conectar,
    )


@pytest.fixture
def app_flask(tmp_path, monkeypatch):
    """O app, apontando para um banco novo e vazio só deste teste."""
    monkeypatch.setenv("DB_PATH", str(tmp_path / "teste.db"))
    monkeypatch.setenv("SECRET_KEY", "chave-de-teste")
    monkeypatch.setenv("ADMIN_USER", "admin")
    monkeypatch.setenv("ADMIN_PASSWORD", "senha-de-teste")

    import app as modulo_app

    flask_app = modulo_app.app
    flask_app.config["DB_PATH"] = tmp_path / "teste.db"
    flask_app.config["TESTING"] = True
    flask_app.config["WTF_CSRF_ENABLED"] = False
    flask_app.config["UPLOAD_FOLDER"] = tmp_path / "uploads"
    modulo_app.limiter.enabled = False

    with flask_app.app_context():
        banco.inicializar_banco()
        usuarios.inicializar_usuarios()

    return flask_app


@pytest.fixture
def produtos(app_flask):
    with app_flask.app_context():
        yield _dados()


@pytest.fixture
def abrir_banco(app_flask):
    """Abre um banco que já existe (ex.: um banco antigo) e roda as migrações."""

    @contextmanager
    def abrir(caminho):
        app_flask.config["DB_PATH"] = caminho
        with app_flask.app_context():
            banco.inicializar_banco()
            yield _dados()

    return abrir


@pytest.fixture
def client_anonimo(produtos, app_flask):
    return app_flask.test_client()


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