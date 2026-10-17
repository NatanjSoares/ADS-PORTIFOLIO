import os
from datetime import timedelta

from flask import (
    Flask, render_template, request, redirect, url_for, flash, session
)
from flask_wtf.csrf import CSRFError, CSRFProtect
import produtos
import usuarios
import dinheiro
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("Defina a variável de ambiente SECRET_KEY.")

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SEGURO") == "1",
    PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
    WTF_CSRF_TIME_LIMIT=None,  # o token vale enquanto a sessão valer
)

csrf = CSRFProtect(app)

usuarios.inicializar_usuarios()

ROTAS_PUBLICAS = {"login", "static"}
limiter = Limiter(get_remote_address, app=app, storage_uri="memory://")

@app.errorhandler(CSRFError)
def csrf_invalido(erro):
    app.logger.warning("CSRF recusado em %s: %s", request.path, erro.description)
    flash("Formulário expirado ou inválido. Tente novamente.", "erro")
    return redirect(url_for("home"))

@app.before_request
def exigir_login():
    if request.endpoint in ROTAS_PUBLICAS:
        return None
    if not session.get("usuario"):
        return redirect(url_for("login"))

def chave_usuario():
    return "usuario:" + request.form.get("usuario", "").strip().lower()


@app.errorhandler(429)
def muitas_tentativas(erro):
    flash("Muitas tentativas. Aguarde alguns minutos e tente de novo.", "erro")
    return render_template("login.html"), 429    



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

def _numero(texto):
    try:
        return float(texto)
    except (TypeError, ValueError):
        return None


def _decimal_ou_none(texto):
    try:
        return dinheiro.para_decimal(texto)
    except ValueError:
        return None


def preco_do_formulario(form):
    custo = _decimal_ou_none(form.get("custo", ""))
    mult = _numero(form.get("multiplicador", ""))
    if custo and mult:
        return produtos.calcular_preco(custo, mult)
    return _decimal_ou_none(form.get("preco", ""))


@app.context_processor
def injetar_multiplicadores():
    return {"multiplicadores": produtos.listar_multiplicadores()}


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
            preco=preco_do_formulario(request.form),
            estoque=int(request.form["estoque"]),
            descricao=request.form["descricao"].strip(),
        
            custo=_decimal_ou_none(request.form.get("custo", "")) or 0,
            multiplicador=_numero(request.form.get("multiplicador", "")) or 0,
        )

        flash("Produto cadastrado com sucesso.", "sucesso")

        return redirect(url_for("listar"))

    return render_template(
        "form.html",
        produto=None,
        titulo="Novo produto"
    )


@app.route("/editar/<int:produto_id>", methods=["GET", "POST"])
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
                produto={**request.form, "id": produto_id},
                titulo="Editar produto"
            )

        
          
        produtos.atualizar(
            produto_id,
            nome=request.form["nome"].strip(),
            categoria=request.form["categoria"].strip(),
            preco=preco_do_formulario(request.form),
            estoque=int(request.form["estoque"]),
            descricao=request.form["descricao"].strip(),
            custo=_decimal_ou_none(request.form.get("custo", "")) or 0,
            multiplicador=_numero(request.form.get("multiplicador", "")) or 0,
        )

        flash("Produto atualizado com sucesso.", "sucesso")

        return redirect(url_for("listar"))

    return render_template(
        "form.html",
        produto=produto,
        titulo="Editar produto"
    )


@app.route("/excluir/<int:produto_id>", methods=["POST"])
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
    custo = form.get("custo", "").strip()
    mult = form.get("multiplicador", "").strip()

    if not nome:
        return "O nome do produto é obrigatório."

    if not categoria:
        return "A categoria é obrigatória."

    if custo or mult:
        valor_custo = _decimal_ou_none(custo)
        valor_mult = _numero(mult)

        if valor_custo is None or valor_custo < 0:
            return "Informe um custo válido."

        if valor_mult is None or not (
            produtos.MULT_MIN <= valor_mult <= produtos.MULT_MAX
        ):
            return "O multiplicador deve estar entre 1,5 e 4."
    else:
        if not preco:
            return "O preço é obrigatório."

        valor_preco = _decimal_ou_none(preco)

        if valor_preco is None:
            return "Informe um preço válido."

        if valor_preco < 0:
            return "O preço não pode ser negativo."

    if not estoque:
        return "O estoque é obrigatório."

    try:
        if int(estoque) < 0:
            return "O estoque não pode ser negativo."
    except ValueError:
        return "Informe um estoque válido."

    if not descricao:
        return "A descrição é obrigatória."

    return None


@app.route("/multiplicadores", methods=["GET", "POST"])
def multiplicadores_view():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        valor = _numero(request.form.get("valor", ""))
        mult_id = request.form.get("id")

        if not nome:
            flash("O nome do multiplicador é obrigatório.", "erro")
        elif valor is None or not (produtos.MULT_MIN <= valor <= produtos.MULT_MAX):
            flash("O valor deve estar entre 1,5 e 4.", "erro")
        else:
            if mult_id:
                produtos.atualizar_multiplicador(int(mult_id), nome, valor)
            else:
                produtos.criar_multiplicador(nome, valor)
            flash("Multiplicador salvo.", "sucesso")
        return redirect(url_for("multiplicadores_view"))

    return render_template("multiplicadores.html")


@app.route("/multiplicadores/<int:mult_id>/excluir", methods=["POST"])
def excluir_multiplicador(mult_id):
    produtos.excluir_multiplicador(mult_id)
    flash("Multiplicador excluído.", "sucesso")
    return redirect(url_for("multiplicadores_view"))

@app.route("/dashboard")
def dashboard():
    itens = produtos.listar_todos()
    com_custo = [p for p in itens if p["custo"]]

    categorias = {}
    for p in itens:
        categorias[p["categoria"]] = categorias.get(p["categoria"], 0) + 1

    margens = [
        (p["preco"] - p["custo"]) / p["preco"] * 100
        for p in com_custo
        if p["preco"]
    ]

    dados = {
        "nomes": [p["nome"] for p in itens],
        "estoque": [p["estoque"] for p in itens],
        "custo_nomes": [p["nome"] for p in com_custo],
        "custos": [float(p["custo"]) for p in com_custo],
        "precos": [float(p["preco"]) for p in com_custo],
        "categorias": list(categorias.keys()),
        "qtd_categorias": list(categorias.values()),
    }

    resumo = {
        "total_produtos": len(itens),
        "itens_estoque": sum(p["estoque"] for p in itens),
        "valor_estoque": sum(p["preco"] * p["estoque"] for p in itens),
        "margem_media": sum(margens) / len(margens) if margens else None,
    }

    return render_template("dashboard.html", dados=dados, resumo=resumo)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,
            debug=os.environ.get("FLASK_DEBUG") == "1")