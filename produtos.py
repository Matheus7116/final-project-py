def menu_produtos(conexao):
    while True:
        print("\n=== PRODUTOS ===")
        print("1 - Cadastrar produto")
        print("2 - Ver todos os produtos")
        print("3 - Editar produto")
        print("4 - Excluir produto")
        print("0 - Voltar")

        opcao = input("Escolha: ")

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
    nome = input("Nome: ")
    marca = input("Marca: ")
    preco = input("Preco: ")
    qtde_estoque = input("Quantidade em estoque: ")
    cursor.execute(f"""
        INSERT INTO produtos (nome, marca, preco, qtde_estoque)
        VALUES ('{nome}', '{marca}', '{preco}', '{qtde_estoque}')
    """)
    conexao.commit()
    cursor.close()
    print(f"Produto {nome} cadastrado com sucesso")

def verprodutos(conexao):
    cursor = conexao.cursor(dictionary=True)
    cursor.execute('SELECT * FROM produtos')
    for element in cursor.fetchall():
        print(f"""
        INFORMAÇÕES DO PRODUTO {element['id']}
        Nome: {element['nome']}
        Marca: {element['marca']}
        Preço: {element['preco']}
        Quantidade em estoque: {element['qtde_estoque']}
    """)
    cursor.close()

def excluirprod(conexao):
    cursor = conexao.cursor(dictionary=True)
    id = int(input("Digite o id do produto que deseja excluir: "))
    cursor.execute(f"DELETE FROM produtos WHERE id = {id}")
    conexao.commit()
    cursor.close()
    print("Produto deletado com sucesso")

def editarprod(conexao):
    cursor = conexao.cursor(dictionary=True)
    id = int(input("Digite o id do produto que deseja editar: "))
    
    cursor.execute(f"SELECT * FROM produtos WHERE id = {id}")
    produto = cursor.fetchone()
    
    if produto:
        novo_nome = input(f"Nome ({produto['nome']}): ") 
        nova_marca = input(f"Marca ({produto['marca']}): ") 
        novo_preco = input(f"Preço ({produto['preco']}): ") 
        nova_qtde = input(f"Quantidade ({produto['qtde_estoque']}): ") 

        cursor.execute(f"""
            UPDATE produtos
            SET nome = '{novo_nome}', marca = '{nova_marca}', preco = '{novo_preco}', qtde_estoque = '{nova_qtde}'
            WHERE id = {id}
        """)
        conexao.commit()
        print("Produto atualizado com sucesso")
    else:
        print("Produto não encontrado")
    
    cursor.close()