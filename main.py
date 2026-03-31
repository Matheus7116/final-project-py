import mysql.connector
import os
from dotenv import load_dotenv
from produtos import menu_produtos 
from funcionarios import menu_funcionarios
from clientes import menu_clientes
from vendas import menu_vendas

load_dotenv() 

conexao = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
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
            menu_funcionarios(conexao)
        if opcao == "3":
            menu_clientes(conexao)
        if opcao == "4":
            menu_vendas(conexao)
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

    conexao.close()

menu()