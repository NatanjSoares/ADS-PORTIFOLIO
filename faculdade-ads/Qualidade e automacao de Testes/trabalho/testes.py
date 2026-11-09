import unittest

from main import maximo

class TesteMaximo(unittest.TestCase):

    # CT01 - Primeiro número menor que o segundo
    def test_primeiro_numero_menor(self):
        resultado = maximo(10, 20)

        self.assertEqual(
            resultado,
            "O número 20 é o maior."
        )

    # CT02 - Primeiro número maior que o segundo
    def test_primeiro_numero_maior(self):
        resultado = maximo(390, 380)

        self.assertEqual(
            resultado,
            "O número 390 é o maior."
        )

    # CT03 - Números iguais
    def test_numeros_iguais(self):
        resultado = maximo(50, 50)

        self.assertEqual(
            resultado,
            "Os dois números são iguais."
        )

if __name__ == "__main__":
    unittest.main()
    