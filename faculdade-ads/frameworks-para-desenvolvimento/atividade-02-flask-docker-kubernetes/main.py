from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resultado', methods=['POST'])
def resultado():
    try:
        salario = float(request.form['salario'])
        dependentes = int(request.form['dependentes'])
        
        # Validação de valores negativos
        if salario < 0 or dependentes < 0:
            return "Erro: Insira valores válidos."
            
    except ValueError:
        # Tratamento de entradas não numéricas
        return "Erro: Insira valores válidos."

    # Regras de Negócio:
    # 1. INSS: alíquota fixa de 8% sobre o salário bruto
    inss = salario * 0.08
    
    # 2. IR: alíquota de 15% apenas se salário bruto > R$ 2.500,00
    ir = salario * 0.15 if salario > 2500 else 0.0
    
    # 3. Dependentes: acréscimo/dedução de R$ 200,00 por dependente
    deducao_dependentes = dependentes * 200.0
    
    # 4. Cálculo final do salário líquido
    salario_liquido = salario - inss - ir + deducao_dependentes


    return render_template('resultados.html',salario_liquido=f"{salario_liquido:.2f}")

if __name__ == '__main__':
    app.run(debug=True)