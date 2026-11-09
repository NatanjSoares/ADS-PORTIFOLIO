def maximo(a, b):
    """
    Compara dois números e identifica o maior valor.
    """

    if a > b:
        return f"O número {a} é o maior."

    elif b > a:
        return f"O número {b} é o maior."

    else:
        return "Os dois números são iguais."

# Execução dos três cenários
if __name__ == "__main__":

    print("TESTE 01")
    print(maximo(10, 20))

    print("\nTESTE 02")
    print(maximo(390, 380))

    print("\nTESTE 03")
    print(maximo(50, 50))
    