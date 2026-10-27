"""Multiplicadores: tela de cadastro, edição e exclusão."""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from adonai.dados import multiplicadores
from adonai.regras import dinheiro
from adonai.regras.validacao import numero_ou_none

bp = Blueprint("multiplicadores", __name__)


@bp.app_context_processor
def injetar_multiplicadores():
    return {"multiplicadores": multiplicadores.listar_multiplicadores()}


@bp.route("/multiplicadores", methods=["GET", "POST"])
def multiplicadores_view():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        valor = numero_ou_none(request.form.get("valor", ""))
        mult_id = request.form.get("id")

        if not nome:
            flash("O nome do multiplicador é obrigatório.", "erro")
        elif valor is None or not (dinheiro.MULT_MIN <= valor <= dinheiro.MULT_MAX):
            flash("O valor deve estar entre 1,5 e 4.", "erro")
        else:
            if mult_id:
                multiplicadores.atualizar_multiplicador(int(mult_id), nome, valor)
            else:
                multiplicadores.criar_multiplicador(nome, valor)
            flash("Multiplicador salvo.", "sucesso")
        return redirect(url_for("multiplicadores.multiplicadores_view"))

    return render_template("multiplicadores.html")


@bp.route("/multiplicadores/<int:mult_id>/excluir", methods=["POST"])
def excluir_multiplicador(mult_id):
    multiplicadores.excluir_multiplicador(mult_id)
    flash("Multiplicador excluído.", "sucesso")
    return redirect(url_for("multiplicadores.multiplicadores_view"))