def menu_produtos(conexao):
    while True:
        print("\n=== PRODUTOS ===")
        print("1 - Cadastrar produto")
        print("2 - Ver todos os produtos")
        print("3 - Editar produto")
        print("4 - Excluir produto")
        print("0 - Voltar")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_produto(conexao)
        elif opcao == "2":
            verprodutos(conexao)
        elif opcao == "3":
            editarprod(conexao)
        elif opcao == "4":
            excluirprod(conexao)
        elif opcao == "0":
            print("Voltando...")
            break
        else:
            print("Opção inválida!")


def cadastrar_produto(conexao):
    cursor = conexao.cursor(dictionary=True)

    nome = input("Nome: ").strip()
    marca = input("Marca: ").strip()
    preco = input("Preco: ").strip()
    qtde_estoque = input("Quantidade em estoque: ").strip()

    if not nome or not marca or not preco or not qtde_estoque:
        print("Erro: nenhum campo pode ficar em branco.")
        cursor.close()
        return

    try:
        preco = float(preco)
    except ValueError:
        print("Erro: preço inválido.")
        cursor.close()
        return

    try:
        qtde_estoque = int(qtde_estoque)
    except ValueError:
        print("Erro: quantidade em estoque inválida.")
        cursor.close()
        return

    if preco < 0:
        print("Erro: o preço não pode ser menor que zero.")
        cursor.close()
        return

    if qtde_estoque < 0:
        print("Erro: a quantidade em estoque não pode ser menor que zero.")
        cursor.close()
        return

    try:
        sql = """
            INSERT INTO produtos (nome, marca, preco, qtde_estoque)
            VALUES (%s, %s, %s, %s)
        """
        valores = (nome, marca, preco, qtde_estoque)
        cursor.execute(sql, valores)
        conexao.commit()
        print(f"Produto {nome} cadastrado com sucesso")
    except Exception as erro:
        print(f"Erro ao cadastrar produto: {erro}")

    cursor.close()


def verprodutos(conexao):
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()

        if not produtos:
            print("Nenhum produto cadastrado.")
        else:
            for element in produtos:
                print(f"""
INFORMAÇÕES DO PRODUTO {element['id']}
Nome: {element['nome']}
Marca: {element['marca']}
Preço: {element['preco']}
Quantidade em estoque: {element['qtde_estoque']}
""")
    except Exception as erro:
        print(f"Erro ao buscar produtos: {erro}")

    cursor.close()


def excluirprod(conexao):
    cursor = conexao.cursor(dictionary=True)

    entrada = input("Digite o id do produto que deseja excluir: ").strip()

    if not entrada:
        print("Erro: o id não pode ficar em branco.")
        cursor.close()
        return

    try:
        id_produto = int(entrada)
    except ValueError:
        print("Erro: digite um id válido.")
        cursor.close()
        return

    try:
        cursor.execute("DELETE FROM produtos WHERE id = %s", (id_produto,))
        conexao.commit()

        if cursor.rowcount > 0:
            print("Produto deletado com sucesso")
        else:
            print("Produto não encontrado")
    except Exception as erro:
        if "foreign key constraint fails" in str(erro).lower():
            print("Não é possível excluir este produto, pois ele está vinculado a uma venda.")
        else:
            print(f"Erro ao excluir produto: {erro}")

    cursor.close()


def editarprod(conexao):
    cursor = conexao.cursor(dictionary=True)

    entrada = input("Digite o id do produto que deseja editar: ").strip()

    if not entrada:
        print("Erro: o id não pode ficar em branco.")
        cursor.close()
        return

    try:
        id_produto = int(entrada)
    except ValueError:
        print("Erro: digite um id válido.")
        cursor.close()
        return

    try:
        cursor.execute("SELECT * FROM produtos WHERE id = %s", (id_produto,))
        produto = cursor.fetchone()

        if not produto:
            print("Produto não encontrado")
            cursor.close()
            return

        novo_nome = input(f"Nome ({produto['nome']}): ").strip()
        nova_marca = input(f"Marca ({produto['marca']}): ").strip()
        novo_preco = input(f"Preço ({produto['preco']}): ").strip()
        nova_qtde = input(f"Quantidade ({produto['qtde_estoque']}): ").strip()

        if novo_nome == "":
            novo_nome = produto['nome']
        if nova_marca == "":
            nova_marca = produto['marca']
        if novo_preco == "":
            novo_preco = produto['preco']
        else:
            try:
                novo_preco = float(novo_preco)
            except ValueError:
                print("Erro: preço inválido.")
                cursor.close()
                return

            if novo_preco < 0:
                print("Erro: o preço não pode ser menor que zero.")
                cursor.close()
                return

        if nova_qtde == "":
            nova_qtde = produto['qtde_estoque']
        else:
            try:
                nova_qtde = int(nova_qtde)
            except ValueError:
                print("Erro: quantidade inválida.")
                cursor.close()
                return

            if nova_qtde < 0:
                print("Erro: a quantidade não pode ser menor que zero.")
                cursor.close()
                return

        sql = """
            UPDATE produtos
            SET nome = %s, marca = %s, preco = %s, qtde_estoque = %s
            WHERE id = %s
        """
        valores = (novo_nome, nova_marca, novo_preco, nova_qtde, id_produto)

        cursor.execute(sql, valores)
        conexao.commit()
        print("Produto atualizado com sucesso")
    except Exception as erro:
        print(f"Erro ao editar produto: {erro}")

    cursor.close()