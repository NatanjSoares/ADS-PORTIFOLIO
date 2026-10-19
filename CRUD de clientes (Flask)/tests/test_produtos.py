def test_banco_novo_tem_dois_produtos(produtos):
    assert len(produtos.listar_todos()) == 2


def test_criar_e_buscar_por_id(produtos):
    novo = produtos.criar("Anel de prata", "Joia", 100.0, 5, "Tamanho 17")
    achado = produtos.buscar_por_id(novo["id"])
    assert achado["nome"] == "Anel de prata"
    assert achado["estoque"] == 5


def test_buscar_por_nome(produtos):
    produtos.criar("Colar de aço", "Joia", 90.0, 1, "45cm")
    resultado = produtos.buscar_por_nome("colar")
    assert len(resultado) == 1
    assert resultado[0]["nome"] == "Colar de aço"


def test_atualizar(produtos):
    novo = produtos.criar("Brinco", "Joia", 50.0, 3, "Pequeno")
    produtos.atualizar(novo["id"], "Brinco grande", "Joia", 60.0, 2, "Grande")
    assert produtos.buscar_por_id(novo["id"])["nome"] == "Brinco grande"


def test_excluir(produtos):
    novo = produtos.criar("Pulseira", "Joia", 40.0, 4, "Fina")
    assert produtos.excluir(novo["id"]) is True
    assert produtos.buscar_por_id(novo["id"]) is None
    assert produtos.excluir(novo["id"]) is False

def test_preco_calculado_pelo_multiplicador(produtos):
    novo = produtos.criar("Anel", "Joia", 0, 1, "x", custo=20.0, multiplicador=2.5)
    assert novo["preco"] == 50.0

def test_multiplicador_fora_da_faixa_e_rejeitado(client):
    resposta = client.post("/novo", data={
        "nome": "Anel", "categoria": "Joia", "custo": "20",
        "multiplicador": "5", "estoque": "1", "descricao": "x",
    })
    assert "entre 1,5 e 4" in resposta.get_data(as_text=True)

def test_produto_novo_nao_tem_foto(produtos):
    novo = produtos.criar("Anel", "Joia", 10, 1, "x")
    assert novo["foto"] is None


def test_criar_com_foto(produtos):
    novo = produtos.criar("Anel", "Joia", 10, 1, "x", foto="abc.jpg")
    assert novo["foto"] == "abc.jpg"


def test_definir_foto_e_remover(produtos):
    novo = produtos.criar("Anel", "Joia", 10, 1, "x")

    produtos.definir_foto(novo["id"], "abc.jpg")
    assert produtos.buscar_por_id(novo["id"])["foto"] == "abc.jpg"

    produtos.definir_foto(novo["id"], None)
    assert produtos.buscar_por_id(novo["id"])["foto"] is None


def test_atualizar_nao_mexe_na_foto(produtos):
    novo = produtos.criar("Anel", "Joia", 10, 1, "x", foto="abc.jpg")
    produtos.atualizar(novo["id"], "Anel 2", "Joia", 20, 2, "y")
    assert produtos.buscar_por_id(novo["id"])["foto"] == "abc.jpg"


def test_banco_em_centavos_ganha_coluna_foto(tmp_path, monkeypatch):
    import importlib
    import sqlite3

    caminho = tmp_path / "sem_foto.db"
    con = sqlite3.connect(caminho)
    con.execute(
        """
        CREATE TABLE produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL, categoria TEXT NOT NULL,
            preco_centavos INTEGER NOT NULL, estoque INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            custo_centavos INTEGER NOT NULL DEFAULT 0,
            multiplicador REAL NOT NULL DEFAULT 0
        )
        """
    )
    con.execute(
        "INSERT INTO produtos (nome, categoria, preco_centavos, estoque,"
        " descricao) VALUES ('Anel','Joia',1990,2,'x')"
    )
    con.commit()
    con.close()

    monkeypatch.setenv("DB_PATH", str(caminho))
    import produtos

    importlib.reload(produtos)

    anel = produtos.buscar_por_nome("Anel")[0]
    assert anel["foto"] is None
    assert anel["preco_centavos"] == 1990
    assert anel["estoque"] == 2


def test_banco_antigo_em_reais_tambem_ganha_foto(tmp_path, monkeypatch):
    import importlib
    import sqlite3

    caminho = tmp_path / "antigo.db"
    con = sqlite3.connect(caminho)
    con.execute(
        """
        CREATE TABLE produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL, categoria TEXT NOT NULL,
            preco REAL NOT NULL, estoque INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            custo REAL NOT NULL DEFAULT 0,
            multiplicador REAL NOT NULL DEFAULT 0
        )
        """
    )
    con.execute(
        "INSERT INTO produtos (nome, categoria, preco, estoque, descricao)"
        " VALUES ('Anel','Joia',19.9,2,'x')"
    )
    con.commit()
    con.close()

    monkeypatch.setenv("DB_PATH", str(caminho))
    import produtos

    importlib.reload(produtos)

    anel = produtos.buscar_por_nome("Anel")[0]
    assert anel["foto"] is None
    assert anel["preco_centavos"] == 1990