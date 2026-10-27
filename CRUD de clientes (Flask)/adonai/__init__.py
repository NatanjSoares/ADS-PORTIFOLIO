"""Pacote do sistema: aqui nasce o app (create_app)."""

from flask import Flask

from adonai.config import RAIZ, carregar_config
from adonai.extensoes import csrf, limiter
from adonai.seguranca import registrar as registrar_seguranca


def create_app(config=None):
    """Monta e devolve um app novo.

    `config` é opcional: um dicionário com valores que sobrescrevem a
    configuração padrão (usado pelos testes).
    """
    app = Flask(
        __name__,
        template_folder=str(RAIZ / "templates"),
        static_folder=str(RAIZ / "static"),
    )

    app.config.from_mapping(carregar_config())
    if config:
        app.config.update(config)

    csrf.init_app(app)
    limiter.init_app(app)
    registrar_seguranca(app)

    # Importados aqui dentro para evitar importação circular.
    from adonai.dados import banco, usuarios
    from adonai.rotas import auth
    from adonai.rotas import dashboard as rotas_dashboard
    from adonai.rotas import multiplicadores as rotas_multiplicadores
    from adonai.rotas import produtos as rotas_produtos

    app.register_blueprint(auth.bp)
    app.register_blueprint(rotas_produtos.bp)
    app.register_blueprint(rotas_multiplicadores.bp)
    app.register_blueprint(rotas_dashboard.bp)

    with app.app_context():
        banco.inicializar_banco()
        usuarios.inicializar_usuarios()

    return app