import mysql.connector
from produtos import menu_produtos 
from funcionarios import menu_funcionarios

conexao = mysql.connector.connect(
    host='DB_HOST',
    user='DB_USER',
    password='DB_PASSWORD',
    database='DB_NAME',
)

def menu():
    while True:
        print("\n=== SUPERMERCADO ===")
        print("1 - Ver produtos")
        print("2 - Ver funcionários")
        print("3 - Ver clientes")
        print("4 - Ver vendas")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            menu_produtos(conexao) 
        if opcao == "2":
            print("Em construção...")
        if opcao == "3":
            print("Em construção...")
        if opcao == "4":
            print("Em construção...")
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

    conexao.close()

menu()