import re

from ajudantes import (
    RAIZ,
)


def test_arquivos_citados_nos_templates_existem():
    padrao = re.compile(r"""filename\s*=\s*['"]([^'"]+)['"]""")
    faltando = []

    for template in (RAIZ / "templates").glob("*.html"):
        texto = template.read_text(encoding="utf-8")
        for nome in padrao.findall(texto):
            if nome.endswith("/"):
                continue  # pasta montada na hora (ex.: uploads/)
            if not (RAIZ / "static" / nome).exists():
                faltando.append(f"{template.name}: static/{nome}")

    assert faltando == []


def test_arquivos_citados_nos_css_existem():
    padrao = re.compile(r"""url\(\s*['"]?([^'")]+)['"]?\s*\)""")
    faltando = []

    for css in (RAIZ / "static" / "css").glob("*.css"):
        texto = css.read_text(encoding="utf-8")
        for caminho in padrao.findall(texto):
            if caminho.startswith(("http", "data:", "#")):
                continue
            if not (css.parent / caminho).resolve().exists():
                faltando.append(f"{css.name}: {caminho}")

    assert faltando == []


def test_main_css_importa_o_css_das_fotos():
    texto = (RAIZ / "static" / "css" / "main.css").read_text(encoding="utf-8")
    assert "foto.css" in texto


def test_main_css_importa_todos_os_modulos():
    pasta = RAIZ / "static" / "css"
    texto = (pasta / "main.css").read_text(encoding="utf-8")

    importados = set(re.findall(r"""@import\s+url\(\s*['"]?([^'")]+)['"]?\s*\)""", texto))
    modulos = {p.name for p in pasta.glob("*.css")} - {"main.css"}

    assert modulos - importados == set()


def test_preco_js_soma_a_embalagem():
    texto = (RAIZ / "static" / "js" / "preco.js").read_text(encoding="utf-8")
    assert "embalagem" in texto


def test_css_dos_ajustes_visuais():
    css = RAIZ / "static" / "css"

    assert "a.botao" in (css / "components.css").read_text(encoding="utf-8")
    assert "white-space: nowrap" in (css / "tabela.css").read_text(encoding="utf-8")
    assert ".grafico-caixa" in (css / "graficos.css").read_text(encoding="utf-8")


def test_dashboard_js_nao_prende_a_proporcao_dos_graficos():
    js = (RAIZ / "static" / "js" / "dashboard.js").read_text(encoding="utf-8")

    assert "maintainAspectRatio" in js
