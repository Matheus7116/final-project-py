import mysql.connector
from produtos import menu_produtos 

conexao = mysql.connector.connect(
    host='localhost',
    user='root',
    password='hercules123.Batata',
    database='SUPERMERCADO',
)

def menu():
    while True:
        print("\n=== SUPERMERCADO ===")
        print("1 - Ver produtos")
        print("2 - Ver clientes")
        print("3 - Ver funcionários")
        print("4 - Ver vendas")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            menu_produtos(conexao) 
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

    conexao.close()

menu()