"""Regras de validação do formulário de produtos (sem Flask e sem banco)."""

from adonai.regras import dinheiro


def numero_ou_none(texto):
    try:
        return float(texto)
    except (TypeError, ValueError):
        return None


def decimal_ou_none(texto):
    try:
        return dinheiro.para_decimal(texto)
    except ValueError:
        return None


def preco_do_formulario(form):
    custo = decimal_ou_none(form.get("custo", ""))
    mult = numero_ou_none(form.get("multiplicador", ""))
    embalagem = decimal_ou_none(form.get("embalagem", "")) or 0

    if custo and mult:
     return dinheiro.calcular_preco(custo, mult, embalagem)
    return decimal_ou_none(form.get("preco", ""))


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
        valor_custo = decimal_ou_none(custo)
        valor_mult = numero_ou_none(mult)

        if valor_custo is None or valor_custo < 0:
            return "Informe um custo válido."

        if valor_mult is None or not (
            dinheiro.MULT_MIN <= valor_mult <= dinheiro.MULT_MAX
        ):
            return "O multiplicador deve estar entre 1,5 e 4."
    else:
        if not preco:
            return "O preço é obrigatório."

        valor_preco = decimal_ou_none(preco)

        if valor_preco is None:
            return "Informe um preço válido."

        if valor_preco < 0:
            return "O preço não pode ser negativo."
    
    embalagem = form.get("embalagem", "").strip()
    frete = form.get("frete", "").strip()

    if embalagem:
        valor_embalagem = decimal_ou_none(embalagem)
        if valor_embalagem is None:
            return "Informe um valor válido para a embalagem."
        if valor_embalagem < 0:
            return "A embalagem não pode ser negativa."

    if frete:
        valor_frete = decimal_ou_none(frete)
        if valor_frete is None:
            return "Informe um valor válido para o frete."
        if valor_frete < 0:
            return "O frete não pode ser negativo."

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
def campos_do_produto(form):
    """Converte o formulário nos campos que o banco recebe (sem a foto)."""
    return {
        "nome": form["nome"].strip(),
        "categoria": form["categoria"].strip(),
        "preco": preco_do_formulario(form),
        "estoque": int(form["estoque"]),
        "descricao": form["descricao"].strip(),
        "custo": decimal_ou_none(form.get("custo", "")) or 0,
        "multiplicador": numero_ou_none(form.get("multiplicador", "")) or 0,
        "embalagem": decimal_ou_none(form.get("embalagem", "")) or 0,
        "frete": decimal_ou_none(form.get("frete", "")) or 0,
    }