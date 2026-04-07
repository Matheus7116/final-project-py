from datetime import datetime

def menu_vendas(conexao):
    while True:
        print("\n=== VENDAS ===")
        print("1 - Realizar venda")
        print("2 - Ver todas as vendas")
        print("0 - Voltar")

        opcao = input("Escolha: ").strip()

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

    entrada_cliente = input("ID do cliente: ").strip()
    entrada_funcionario = input("ID do funcionário: ").strip()
    entrada_produto = input("ID do produto: ").strip()
    entrada_qtde = input("Quantidade: ").strip()

    if not entrada_cliente or not entrada_funcionario or not entrada_produto or not entrada_qtde:
        print("Erro: nenhum campo pode ficar em branco.")
        cursor.close()
        return

    try:
        id_cliente = int(entrada_cliente)
        id_funcionario = int(entrada_funcionario)
        id_produto = int(entrada_produto)
        qtde_comprada = int(entrada_qtde)
    except ValueError:
        print("Erro: digite apenas números válidos.")
        cursor.close()
        return

    if qtde_comprada <= 0:
        print("Erro: a quantidade deve ser maior que zero.")
        cursor.close()
        return

    try:
        cursor.execute("SELECT id FROM clientes WHERE id = %s", (id_cliente,))
        cliente = cursor.fetchone()

        if not cliente:
            print("Cliente não encontrado.")
            cursor.close()
            return

        cursor.execute("SELECT id FROM funcionarios WHERE id = %s", (id_funcionario,))
        funcionario = cursor.fetchone()

        if not funcionario:
            print("Funcionário não encontrado.")
            cursor.close()
            return

        cursor.execute("SELECT id, preco FROM produtos WHERE id = %s", (id_produto,))
        produto = cursor.fetchone()

        if not produto:
            print("Produto não encontrado.")
            cursor.close()
            return

        data_venda = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        valor_total = produto['preco'] * qtde_comprada

        sql = """
            INSERT INTO vendas (id_cliente, data_venda, id_funcionario, id_produto, qtde_comprada, valor_total)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (id_cliente, data_venda, id_funcionario, id_produto, qtde_comprada, valor_total)

        cursor.execute(sql, valores)
        conexao.commit()

        print(f"Venda realizada com sucesso! Total: R$ {valor_total:.2f}")

    except Exception as erro:
        print(f"Erro ao realizar venda: {erro}")

    cursor.close()


def ver_vendas(conexao):
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM vendas")
        vendas = cursor.fetchall()

        if not vendas:
            print("Nenhuma venda registrada.")
        else:
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
    except Exception as erro:
        print(f"Erro ao buscar vendas: {erro}")

    cursor.close()