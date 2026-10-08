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