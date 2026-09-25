import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

import static org.junit.jupiter.api.Assertions.*;

class CalculadoraTest {

    private Calculadora calculadora;

    @BeforeEach
    void configurar() {
        calculadora = new Calculadora();
    }

    @Test
    void deveSomarDoisNumeros() {
        double resultado = calculadora.somar(10, 5);



        assertEquals(15, resultado, 0.0001);
    }

    @Test
    void deveSubtrairDoisNumeros() {
        double resultado = calculadora.subtrair(10, 5);

        assertEquals(5, resultado, 0.0001);
    }

    @Test
    void deveMultiplicarDoisNumeros() {
        double resultado = calculadora.multiplicar(10, 5);

        assertEquals(50, resultado, 0.0001);
    }

    @Test
    void deveDividirDoisNumeros() {
        double resultado = calculadora.dividir(10, 2);

        assertEquals(5, resultado, 0.0001);
    }

    @Test
    void deveSomarNumeroNegativo() {
        double resultado = calculadora.somar(-10, 5);

        assertEquals(-5, resultado, 0.0001);
    }

    @Test
    void deveLancarExcecaoAoDividirPorZero() {
        assertThrows(
                ArithmeticException.class,
                () -> calculadora.dividir(10, 0)
        );
    }

    @ParameterizedTest
    @CsvSource({
            "2, 3, 5",
            "10, 5, 15",
            "-5, 5, 0",
            "20, 10, 30"
    })
    void deveSomarValores(double a, double b, double esperado) {

        double resultado = calculadora.somar(a, b);

        assertEquals(esperado, resultado, 0.0001);
    }
}