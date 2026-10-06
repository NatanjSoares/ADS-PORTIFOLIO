from flask import Flask, render_template, request, redirect, url_for, flash

import produtos
import os


app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "dev")


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/produtos")
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


@app.route("/home.html/novo", methods=["GET", "POST"])
def novo():
    """CREATE — cadastra um novo produto."""

    if request.method == "POST":

        erro = validar_formulario(request.form)

        if erro:
            flash(erro, "erro")

            return render_template(
                "form.html",
                produto=request.form,
                titulo="Novo produto"
            )

        produtos.criar(
            nome=request.form["nome"].strip(),
            categoria=request.form["categoria"].strip(),
            preco=float(request.form["preco"]),
            estoque=int(request.form["estoque"]),
            descricao=request.form["descricao"].strip()
        )

        flash("Produto cadastrado com sucesso.", "sucesso")

        return redirect(url_for("listar"))

    return render_template(
        "form.html",
        produto=None,
        titulo="Novo produto"
    )


@app.route("/home.html/editar/<int:produto_id>", methods=["GET", "POST"])
def editar(produto_id):
    """UPDATE — edita um produto existente."""

    produto = produtos.buscar_por_id(produto_id)

    if produto is None:
        flash("Produto não encontrado.", "erro")

        return redirect(url_for("listar"))

    if request.method == "POST":

        erro = validar_formulario(request.form)

        if erro:
            flash(erro, "erro")

            return render_template(
                "form.html",
                produto=request.form,
                titulo="Editar produto"
            )

        produtos.atualizar(
            produto_id,
            nome=request.form["nome"].strip(),
            categoria=request.form["categoria"].strip(),
            preco=float(request.form["preco"]),
            estoque=int(request.form["estoque"]),
            descricao=request.form["descricao"].strip()
        )

        flash("Produto atualizado com sucesso.", "sucesso")

        return redirect(url_for("listar"))

    return render_template(
        "form.html",
        produto=produto,
        titulo="Editar produto"
    )


@app.route("/listar.html/excluir/<int:produto_id>", methods=["POST"])
def excluir(produto_id):
    """DELETE — remove um produto."""

    if produtos.excluir(produto_id):
        flash("Produto excluído.", "sucesso")
    else:
        flash("Produto não encontrado.", "erro")

    return redirect(url_for("listar"))


def validar_formulario(form):
    """Validação simples dos dados do produto."""

    nome = form.get("nome", "").strip()
    categoria = form.get("categoria", "").strip()
    preco = form.get("preco", "").strip()
    estoque = form.get("estoque", "").strip()
    descricao = form.get("descricao", "").strip()

    if not nome:
        return "O nome do produto é obrigatório."

    if not categoria:
        return "A categoria é obrigatória."

    if not preco:
        return "O preço é obrigatório."

    try:
        preco = float(preco)

        if preco < 0:
            return "O preço não pode ser negativo."

    except ValueError:
        return "Informe um preço válido."

    if not estoque:
        return "O estoque é obrigatório."

    try:
        estoque = int(estoque)

        if estoque < 0:
            return "O estoque não pode ser negativo."

    except ValueError:
        return "Informe um estoque válido."

    if not descricao:
        return "A descrição é obrigatória."

    return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,
            debug=os.environ.get("FLASK_DEBUG") == "1")