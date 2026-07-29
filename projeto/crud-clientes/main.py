import os

os.system('cls' if os.name == 'nt' else 'clear')

print("====================================")
print(" SISTEMA DE CADASTRO DE CLIENTES ")
print("====================================")

opcao = input("1 - Cadastrar\n2 - Sair\n\nEscolha: ")

if opcao == "1":

    nome = input("Nome: ")
    idade = input("Idade: ")
    email = input("E-mail: ")
    cidade = input("Cidade: ")
    estado = input("Estado (UF): ")
    telefone = input("Telefone: ")

    print("\n===== RESULTADO =====")

    if 5 <= len(nome) <= 35:
        print(f"Nome: {nome}")
    else:
        print("Nome inválido!")

    if idade.isdigit() and 0 < int(idade) <= 120:
        print(f"Idade: {idade}")
    else:
        print("Idade inválida!")

    if "@" in email and "." in email:
        print(f"E-mail: {email}")
    else:
        print("E-mail inválido!")

    if 1 <= len(cidade) <= 50:
        print(f"Cidade: {cidade}")
    else:
        print("Cidade inválida!")

    if len(estado) == 2 and estado.isalpha():
        print(f"Estado: {estado.upper()}")
    else:
        print("Estado inválido!")

    if telefone.isdigit() and len(telefone) in (10, 11):
        print(f"Telefone: {telefone}")
    else:
        print("Telefone inválido!")

elif opcao == "2":
    print("Sistema encerrado.")

else:
    print("Opção inválida!")