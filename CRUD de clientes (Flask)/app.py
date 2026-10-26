import os
from datetime import timedelta

from flask import (
    Flask, render_template, request, redirect, url_for, flash, session
)
from flask_wtf.csrf import CSRFError, CSRFProtect
from adonai.dados import banco, multiplicadores, produtos, usuarios
from adonai.regras import dinheiro
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pathlib import Path

from werkzeug.exceptions import RequestEntityTooLarge

from adonai.regras import fotos
from adonai.regras.estatisticas import calcular_painel
from adonai.regras.validacao import (
    decimal_ou_none,
    numero_ou_none,
    preco_do_formulario,
    validar_formulario,
)
from adonai.config import carregar_config
from adonai.extensoes import csrf, limiter
from adonai.seguranca import registrar as registrar_seguranca
app = Flask(__name__)

app.config.from_mapping(carregar_config())
csrf.init_app(app)
limiter.init_app(app)
registrar_seguranca(app)


with app.app_context():
    banco.inicializar_banco()
    usuarios.inicializar_usuarios()

def chave_usuario():
    return "usuario:" + request.form.get("usuario", "").strip().lower()


@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute; 30 per hour", methods=["POST"])
@limiter.limit("10 per hour", methods=["POST"], key_func=chave_usuario)
def login():
    if session.get("usuario"):
        return redirect(url_for("home"))

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "")

        if usuarios.verificar_login(usuario, senha):
            session.clear()
            session["usuario"] = usuario
            session.permanent = True
            return redirect(url_for("home"))

        flash("Usuário ou senha inválidos.", "erro")

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Você saiu do sistema.", "sucesso")
    return redirect(url_for("login"))



@app.context_processor
def injetar_multiplicadores():
    return {"multiplicadores": multiplicadores.listar_multiplicadores()}


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


@app.route("/novo", methods=["GET", "POST"])
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

        pasta = app.config["UPLOAD_FOLDER"]
        nome_foto = None

        if fotos.tem_foto(foto):
            nome_foto = fotos.salvar_foto(foto, pasta)

        try:
            produtos.criar(
                nome=request.form["nome"].strip(),
                categoria=request.form["categoria"].strip(),
                preco=preco_do_formulario(request.form),
                estoque=int(request.form["estoque"]),
                descricao=request.form["descricao"].strip(),
                custo=decimal_ou_none(request.form.get("custo", "")) or 0,
                multiplicador=numero_ou_none(request.form.get("multiplicador", "")) or 0,
                foto=nome_foto,
                embalagem=decimal_ou_none(request.form.get("embalagem", "")) or 0,
                frete=decimal_ou_none(request.form.get("frete", "")) or 0,
            )
        except Exception:
            fotos.remover_foto(nome_foto, pasta)
            raise

        flash("Produto cadastrado com sucesso.", "sucesso")

        return redirect(url_for("listar"))

    return render_template(
        "form.html",
        produto=None,
        titulo="Novo produto"
    )


@app.route("/editar/<int:produto_id>", methods=["GET", "POST"])
def editar(produto_id):
    """UPDATE — edita um produto existente (e a foto, se for o caso)."""

    produto = produtos.buscar_por_id(produto_id)

    if produto is None:
        flash("Produto não encontrado.", "erro")

        return redirect(url_for("listar"))

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

        pasta = app.config["UPLOAD_FOLDER"]
        foto_antiga = produto["foto"]
        trocar = fotos.tem_foto(foto)
        remover = bool(request.form.get("remover_foto"))
        nova_foto = fotos.salvar_foto(foto, pasta) if trocar else None

        try:
            produtos.atualizar(
                produto_id,
                nome=request.form["nome"].strip(),
                categoria=request.form["categoria"].strip(),
                preco=preco_do_formulario(request.form),
                estoque=int(request.form["estoque"]),
                descricao=request.form["descricao"].strip(),
                custo=decimal_ou_none(request.form.get("custo", "")) or 0,
                multiplicador=numero_ou_none(request.form.get("multiplicador", "")) or 0,
                embalagem=decimal_ou_none(request.form.get("embalagem", "")) or 0,
                frete=decimal_ou_none(request.form.get("frete", "")) or 0,
            )

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

        return redirect(url_for("listar"))

    return render_template(
        "form.html",
        produto=produto,
        titulo="Editar produto"
    )


@app.route("/excluir/<int:produto_id>", methods=["POST"])
def excluir(produto_id):
    """DELETE — remove um produto e a foto dele."""

    produto = produtos.buscar_por_id(produto_id)

    if produto and produtos.excluir(produto_id):
        fotos.remover_foto(produto["foto"], app.config["UPLOAD_FOLDER"])
        flash("Produto excluído.", "sucesso")
    else:
        flash("Produto não encontrado.", "erro")

    return redirect(url_for("listar"))


@app.route("/multiplicadores", methods=["GET", "POST"])
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
        return redirect(url_for("multiplicadores_view"))

    return render_template("multiplicadores.html")


@app.route("/multiplicadores/<int:mult_id>/excluir", methods=["POST"])
def excluir_multiplicador(mult_id):
    multiplicadores.excluir_multiplicador(mult_id)
    flash("Multiplicador excluído.", "sucesso")
    return redirect(url_for("multiplicadores_view"))

@app.route("/dashboard")
def dashboard():
    dados, resumo = calcular_painel(produtos.listar_todos())
    return render_template("dashboard.html", dados=dados, resumo=resumo)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,
            debug=os.environ.get("FLASK_DEBUG") == "1")