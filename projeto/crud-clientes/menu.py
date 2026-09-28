
clientes = []

while True:
    print("====================================")
    print(" SISTEMA DE MENU ")
    print("====================================")
    print("1 - Cadastrar Cliente")
    print("2 - Listar Clientes")
    print("3 - Sair")
    print("4 - Buscar Cliente por Nome")
    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        nome = input("Nome: ")
        idade = input("Idade: ")
        email = input("Email: ")
        cidade = input("Cidade: ")
        cliente = {
            "nome": nome,
            "idade": idade,
            "email": email,
            "cidade": cidade,
        }
        clientes.append(cliente)
        print("\nCliente cadastrado com sucesso!")

    elif opcao == "2":
        if len(clientes) == 0:
            print("\nNenhum cliente cadastrado.")
        else:
            for cliente in clientes:
                print(f"Nome: {cliente['nome']}")
                print(f"Idade: {cliente['idade']}")
                print(f"Email: {cliente['email']}")
                print(f"Cidade: {cliente['cidade']}")
                print("------------------------")
            print(f"\nTotal de clientes: {len(clientes)}")

    elif opcao == "3":
        print("\n===== Sistema encerrado =====")
        break

    elif opcao == "4":
        busca = input("Nome para buscar: ").strip().lower()
        encontrado = False
        for cliente in clientes:
            if busca in cliente["nome"].lower():
                print(f"\nNome: {cliente['nome']}")
                print(f"Idade: {cliente['idade']}")
                print(f"Email: {cliente['email']}")
                print(f"Cidade: {cliente['cidade']}")
                print("------------------------")
                encontrado = True
        if not encontrado:
            print("\nCliente não encontrado.")

    else:
        print("Opção inválida! Tente novamente.")

    print("\nDeseja continuar? (s/n)")
    continuar = input().lower()
    if continuar != "s":
        print("\n===== Sistema encerrado =====")
        break
