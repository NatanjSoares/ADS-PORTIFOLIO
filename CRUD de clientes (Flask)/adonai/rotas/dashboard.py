"""Painel com os números e gráficos dos produtos."""

from flask import Blueprint, render_template

from adonai.dados import produtos
from adonai.regras.estatisticas import calcular_painel

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard")
def dashboard():
    dados, resumo = calcular_painel(produtos.listar_todos())
    return render_template("dashboard.html", dados=dados, resumo=resumo)