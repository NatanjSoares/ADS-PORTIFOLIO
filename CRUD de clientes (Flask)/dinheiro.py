from decimal import ROUND_HALF_UP, Decimal, InvalidOperation

CENTAVO = Decimal("0.01")
LIMITE = Decimal("9999999.99")


def para_decimal(valor):
    """Converte texto, int, float ou Decimal em Decimal com 2 casas.

    Levanta ValueError para valores vazios, inválidos, infinitos ou acima do limite.
    """
    if isinstance(valor, float):
        valor = repr(valor)

    texto = str(valor).strip().replace(",", ".")

    try:
        numero = Decimal(texto)
        if not numero.is_finite():
            raise ValueError
        numero = numero.quantize(CENTAVO, rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        raise ValueError(f"Valor monetário inválido: {valor!r}") from None

    if abs(numero) > LIMITE:
        raise ValueError("Valor acima do limite permitido.")

    return numero


def para_centavos(valor):
    return int(para_decimal(valor) * 100)


def de_centavos(centavos):
    return (Decimal(int(centavos)) / 100).quantize(CENTAVO)


def calcular_preco(custo, multiplicador):
    resultado = para_decimal(custo) * Decimal(str(multiplicador))
    return resultado.quantize(CENTAVO, rounding=ROUND_HALF_UP)