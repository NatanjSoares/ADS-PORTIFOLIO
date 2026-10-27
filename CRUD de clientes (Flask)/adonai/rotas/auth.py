"""Entrada e saída do sistema: login e logout."""

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)

from adonai.dados import usuarios
from adonai.extensoes import limiter

bp = Blueprint("auth", __name__)


def chave_usuario():
    return "usuario:" + request.form.get("usuario", "").strip().lower()


@bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute; 30 per hour", methods=["POST"])
@limiter.limit("10 per hour", methods=["POST"], key_func=chave_usuario)
def login():
    if session.get("usuario"):
        return redirect(url_for("produtos.home"))

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "")

        if usuarios.verificar_login(usuario, senha):
            session.clear()
            session["usuario"] = usuario
            session.permanent = True
            return redirect(url_for("produtos.home"))

        flash("Usuário ou senha inválidos.", "erro")

    return render_template("login.html")


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Você saiu do sistema.", "sucesso")
    return redirect(url_for("auth.login"))