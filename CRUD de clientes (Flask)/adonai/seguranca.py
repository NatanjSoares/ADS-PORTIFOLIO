"""Proteção das páginas: exige login e trata os erros de segurança."""

from flask import flash, redirect, render_template, request, session, url_for
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import RequestEntityTooLarge

ROTAS_PUBLICAS = {"auth.login", "static"}


def registrar(app):
    """Liga ao app a exigência de login e os tratadores de erro."""

    @app.errorhandler(CSRFError)
    def csrf_invalido(erro):
        app.logger.warning("CSRF recusado em %s: %s", request.path, erro.description)
        flash("Formulário expirado ou inválido. Tente novamente.", "erro")
        return redirect(url_for("produtos.home"))

    @app.before_request
    def exigir_login():
        if request.endpoint in ROTAS_PUBLICAS:
            return None
        if not session.get("usuario"):
            return redirect(url_for("auth.login"))

    @app.errorhandler(429)
    def muitas_tentativas(erro):
        flash("Muitas tentativas. Aguarde alguns minutos e tente de novo.", "erro")
        return render_template("login.html"), 429

    @app.errorhandler(RequestEntityTooLarge)
    def arquivo_grande_demais(erro):
        flash("A foto deve ter no máximo 2 MB.", "erro")
        return redirect(request.path)