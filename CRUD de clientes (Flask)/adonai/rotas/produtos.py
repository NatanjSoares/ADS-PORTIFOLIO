"""Rotas de produtos: página inicial, lista, cadastro, edição e exclusão."""

from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, url_for
)

from adonai.dados import produtos
from adonai.regras import fotos
from adonai.regras.validacao import campos_do_produto, validar_formulario

bp = Blueprint("produtos", __name__)


@bp.route("/")
def home():
    return render_template("home.html")


@bp.route("/produtos")
def listar():
    """READ — lista todos os produtos, com busca opcional por nome."""

    termo = request.args.get("q", "").strip()

    dados = (
        produtos.buscar_por_nome(termo)
        if termo
        else produtos.listar_todos()
    )

    return render_template(
        "listar.html",
        produtos=dados,
        termo=termo
    )


@bp.route("/novo", methods=["GET", "POST"])
def novo():
    """CREATE — cadastra um novo produto (a foto é opcional)."""

    if request.method == "POST":

        erro = validar_formulario(request.form)
        foto = request.files.get("foto")

        if not erro:
            erro = fotos.validar_foto(foto)

        if erro:
            flash(erro, "erro")

            return render_template(
                "form.html",
                produto=request.form,
                titulo="Novo produto"
            )

        pasta = current_app.config["UPLOAD_FOLDER"]
        nome_foto = None

        if fotos.tem_foto(foto):
            nome_foto = fotos.salvar_foto(foto, pasta)

        try:
            produtos.criar(**campos_do_produto(request.form), foto=nome_foto)
        except Exception:
            fotos.remover_foto(nome_foto, pasta)
            raise

        flash("Produto cadastrado com sucesso.", "sucesso")

        return redirect(url_for("produtos.listar"))

    return render_template(
        "form.html",
        produto=None,
        titulo="Novo produto"
    )


@bp.route("/editar/<int:produto_id>", methods=["GET", "POST"])
def editar(produto_id):
    """UPDATE — edita um produto existente (e a foto, se for o caso)."""

    produto = produtos.buscar_por_id(produto_id)

    if produto is None:
        flash("Produto não encontrado.", "erro")

        return redirect(url_for("produtos.listar"))

    if request.method == "POST":

        erro = validar_formulario(request.form)
        foto = request.files.get("foto")

        if not erro:
            erro = fotos.validar_foto(foto)

        if erro:
            flash(erro, "erro")

            return render_template(
                "form.html",
                produto={**request.form, "id": produto_id, "foto": produto["foto"]},
                titulo="Editar produto"
            )

        pasta = current_app.config["UPLOAD_FOLDER"]
        foto_antiga = produto["foto"]
        trocar = fotos.tem_foto(foto)
        remover = bool(request.form.get("remover_foto"))
        nova_foto = fotos.salvar_foto(foto, pasta) if trocar else None

        try:
            produtos.atualizar(produto_id, **campos_do_produto(request.form))

            if nova_foto:
                produtos.definir_foto(produto_id, nova_foto)
            elif remover:
                produtos.definir_foto(produto_id, None)
        except Exception:
            fotos.remover_foto(nova_foto, pasta)
            raise

        # só depois que o banco deu certo é seguro apagar a foto antiga
        if nova_foto or remover:
            fotos.remover_foto(foto_antiga, pasta)

        flash("Produto atualizado com sucesso.", "sucesso")

        return redirect(url_for("produtos.listar"))

    return render_template(
        "form.html",
        produto=produto,
        titulo="Editar produto"
    )


@bp.route("/excluir/<int:produto_id>", methods=["POST"])
def excluir(produto_id):
    """DELETE — remove um produto e a foto dele."""

    produto = produtos.buscar_por_id(produto_id)

    if produto and produtos.excluir(produto_id):
        fotos.remover_foto(produto["foto"], current_app.config["UPLOAD_FOLDER"])
        flash("Produto excluído.", "sucesso")
    else:
        flash("Produto não encontrado.", "erro")

    return redirect(url_for("produtos.listar"))