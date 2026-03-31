from datetime import datetime

def menu_vendas(conexao):
    while True:
        print("\n=== VENDAS ===")
        print("1 - Realizar venda")
        print("2 - Ver todas as vendas")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            realizar_venda(conexao)
        elif opcao == "2":
            ver_vendas(conexao)
        elif opcao == "0":
            print("Voltando...")
            break
        else:
            print("Opção inválida!")

def realizar_venda(conexao):
    cursor = conexao.cursor(dictionary=True)
    
    try:
        id_cliente = int(input("ID do cliente: "))
        id_funcionario = int(input("ID do funcionário: "))
        id_produto = int(input("ID do produto: "))
        qtde_comprada = int(input("Quantidade: "))
    except ValueError:
        print("Digite apenas números válidos!")
        cursor.close()
        return

    data_venda = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 

    # Buscar preço do produto
    cursor.execute("SELECT preco FROM produtos WHERE id = %s", (id_produto,))
    produto = cursor.fetchone()

    if produto is None:
        print("Produto não encontrado!")
        cursor.close()
        return

    valor_total = produto['preco'] * qtde_comprada

    # Inserir venda no banco
    cursor.execute("""
        INSERT INTO vendas (id_cliente, data_venda, id_funcionario, id_produto, qtde_comprada, valor_total)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (id_cliente, data_venda, id_funcionario, id_produto, qtde_comprada, valor_total))

    conexao.commit()
    cursor.close()
    print(f"Venda realizada com sucesso! Total: R$ {valor_total:.2f}")

def ver_vendas(conexao):
    cursor = conexao.cursor(dictionary=True)
    cursor.execute('SELECT * FROM vendas')
    vendas = cursor.fetchall()
    cursor.close()

    if not vendas:
        print("Nenhuma venda registrada.")
        return

    for element in vendas:
        print(f"""
INFORMAÇÕES DA VENDA {element['id']}
Data da venda: {element['data_venda']}
ID do cliente: {element['id_cliente']}
ID do funcionário: {element['id_funcionario']}
ID do produto: {element['id_produto']}
Quantidade comprada: {element['qtde_comprada']}
Valor total: R$ {element['valor_total']:.2f}
        """)