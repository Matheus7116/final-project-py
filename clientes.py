def menu_clientes(conexao):
    while True:
        print("\n=== CLIENTES ===")
        print("1 - Cadastrar cliente")
        print("2 - Ver todos os clientes")
        print("3 - Editar cliente")
        print("4 - Excluir cliente")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            cadastrar_cliente(conexao)
        elif opcao == "2":
            ver_clientes(conexao)
        elif opcao == "3":
            editar_cliente(conexao)
        elif opcao == "4":
            excluir_cliente(conexao)
        elif opcao == "0":
            print("Voltando...")
            break
        else:
            print("Opção inválida!")

def cadastrar_cliente(conexao):
    cursor = conexao.cursor(dictionary=True)
    nome = input("Nome: ")
    endereco = input("Endereço: ")
    email = input("Email: ")
    telefone = input("Telefone: ")      
    cursor.execute(f"""
        INSERT INTO clientes (nome, endereco, email, telefone)
        VALUES ('{nome}', '{endereco}', '{email}', '{telefone}')
    """)
    conexao.commit()
    cursor.close()
    print(f"Cliente {nome} cadastrado com sucesso")

def ver_clientes(conexao):
    cursor = conexao.cursor(dictionary=True)
    cursor.execute('SELECT * FROM clientes  ')
    for element in cursor.fetchall():
        print(f"""
        INFORMAÇÕES DO CLIENTE {element['id']}
        Nome: {element['nome']}
        Endereço: {element['endereco']}
        Email: {element['email']}
        Telefone: {element['telefone']}
    """)
    cursor.close()

def excluir_cliente(conexao):
    cursor = conexao.cursor(dictionary=True)
    id = int(input("Digite o id do cliente que deseja excluir: "))
    cursor.execute(f"DELETE FROM clientes WHERE id = {id}")
    conexao.commit()
    cursor.close()
    print("Cliente excluído com sucesso")

def editar_cliente(conexao):
    cursor = conexao.cursor(dictionary=True)
    id = int(input("Digite o id do cliente que deseja editar: "))
    
    cursor.execute(f"SELECT * FROM clientes WHERE id = {id}")
    cliente = cursor.fetchone()
    
    if cliente:
        novo_nome = input(f"Nome ({cliente['nome']}): ") 
        novo_endereco = input(f"Endereço ({cliente['endereco']}): ") 
        novo_email = input(f"Email ({cliente['email']}): ") 
        novo_telefone = input(f"Telefone ({cliente['telefone']}): ") 

        cursor.execute(f"""
            UPDATE clientes
            SET nome = '{novo_nome}', endereco = '{novo_endereco}', email = '{novo_email}', telefone = '{novo_telefone}'
            WHERE id = {id}
        """)
        conexao.commit()
        print("Cliente atualizado com sucesso")
    else:
        print("Cliente não encontrado")

    cursor.close()