# Atividade 02 — Calculadora de salário líquido (Flask + Docker + Kubernetes)

Aplicação web em **Flask** que recebe salário bruto e número de dependentes por formulário (POST), valida os dados no backend e mostra o salário líquido.

## Regras de cálculo

- INSS: 8% sobre o salário bruto
- IR: 15% apenas se o salário bruto for maior que R$ 2.500,00
- Dependentes: R$ 200,00 por dependente, somados ao líquido
- Entradas inválidas (texto ou valores negativos) retornam mensagem de erro

## Estrutura

```text
├── main.py               # rotas e regras de negócio
├── templates/            # index.html (formulário) e resultados.html (Jinja2)
├── static/style.css      # estilo
├── requirements.txt
├── Dockerfile            # python:3.13-slim + gunicorn na porta 5000
├── docker-compose.yml
├── deployment.yaml       # Kubernetes: Deployment com 2 réplicas
├── service.yaml          # Kubernetes: Service LoadBalancer (porta 5000)
└── relatorio-atividade-02.pdf
```

## Tecnologias

Python · Flask · Jinja2 · Gunicorn · Docker · Docker Compose · Kubernetes

## Como executar

**Localmente:**

```bash
pip install -r requirements.txt
python main.py
```

Acesse http://127.0.0.1:5000

**Com Docker Compose:**

```bash
docker compose up --build
```

Acesse http://localhost:5000

**No Kubernetes:** o `deployment.yaml` usa a imagem `natanjsoares/calculadora-salario:latest`, que precisa estar disponível para o cluster (por exemplo, publicada no Docker Hub).

```bash
docker build -t natanjsoares/calculadora-salario:latest .
kubectl apply -f deployment.yaml -f service.yaml
```
