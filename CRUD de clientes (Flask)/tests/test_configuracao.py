from pathlib import Path

RAIZ = Path(__file__).parent.parent


def _ler(nome):
    return (RAIZ / nome).read_text(encoding="utf-8")


def _linhas(nome):
    return [
        linha.strip()
        for linha in _ler(nome).splitlines()
        if linha.strip() and not linha.strip().startswith("#")
    ]


def test_gitignore_protege_segredos_e_dados():
    linhas = _linhas(".gitignore")
    for item in (".env", "*.db", "data/", "static/uploads/*",
                 ".pytest_cache/", "backup/"):
        assert item in linhas, f"falta {item} no .gitignore"


def test_dockerignore_nao_deixa_segredos_nem_dados_entrarem_na_imagem():
    linhas = _linhas(".dockerignore")
    for item in (".env", "*.db", ".git", "data/", "static/uploads/"):
        assert item in linhas, f"falta {item} no .dockerignore"


def test_env_example_nao_traz_valores_preenchidos():
    for linha in _linhas(".env.example"):
        chave, _, valor = linha.partition("=")
        assert valor.strip() == "", f"{chave} está preenchida no .env.example"


def test_env_example_lista_as_variaveis_obrigatorias():
    chaves = {linha.partition("=")[0] for linha in _linhas(".env.example")}
    assert {"SECRET_KEY", "ADMIN_USER", "ADMIN_PASSWORD"} <= chaves


def test_compose_guarda_banco_e_fotos_em_volumes():
    texto = _ler("docker-compose.yml")
    assert "dados:/data" in texto
    assert "fotos:/app/static/uploads" in texto
    assert "env_file" in texto
    assert ".:/app" not in texto  # o código vai na imagem, não montado


def test_dockerfile_aponta_o_banco_para_o_volume():
    assert "DB_PATH=/data/produtos.db" in _ler("Dockerfile")