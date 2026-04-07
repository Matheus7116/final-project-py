def menu_clientes(conexao):
    while True:
        print("\n=== CLIENTES ===")
        print("1 - Cadastrar cliente")
        print("2 - Ver todos os clientes")
        print("3 - Editar cliente")
        print("4 - Excluir cliente")
        print("0 - Voltar")

        opcao = input("Escolha: ").strip()

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

    nome = input("Nome: ").strip()
    endereco = input("Endereço: ").strip()
    email = input("Email: ").strip()
    telefone = input("Telefone: ").strip()

    if not nome or not endereco or not email or not telefone:
        print("Erro: nenhum campo pode ficar em branco.")
        cursor.close()
        return

    try:
        sql = """
            INSERT INTO clientes (nome, endereco, email, telefone)
            VALUES (%s, %s, %s, %s)
        """
        valores = (nome, endereco, email, telefone)
        cursor.execute(sql, valores)
        conexao.commit()
        print(f"Cliente {nome} cadastrado com sucesso")
    except Exception as erro:
        print(f"Erro ao cadastrar cliente: {erro}")

    cursor.close()


def ver_clientes(conexao):
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()

        if not clientes:
            print("Nenhum cliente cadastrado.")
        else:
            for element in clientes:
                print(f"""
INFORMAÇÕES DO CLIENTE {element['id']}
Nome: {element['nome']}
Endereço: {element['endereco']}
Email: {element['email']}
Telefone: {element['telefone']}
""")
    except Exception as erro:
        print(f"Erro ao buscar clientes: {erro}")

    cursor.close()


def excluir_cliente(conexao):
    cursor = conexao.cursor(dictionary=True)

    entrada = input("Digite o id do cliente que deseja excluir: ").strip()

    if not entrada:
        print("Erro: o id não pode ficar em branco.")
        cursor.close()
        return

    try:
        id_cliente = int(entrada)
    except ValueError:
        print("Erro: digite um id válido.")
        cursor.close()
        return

    try:
        cursor.execute("DELETE FROM clientes WHERE id = %s", (id_cliente,))
        conexao.commit()

        if cursor.rowcount > 0:
            print("Cliente excluído com sucesso")
        else:
            print("Cliente não encontrado")
    except Exception as erro:
        if "foreign key constraint fails" in str(erro).lower():
            print("Não é possível excluir este cliente, pois ele está vinculado a uma venda.")
        else:
            print(f"Erro ao excluir cliente: {erro}")

    cursor.close()


def editar_cliente(conexao):
    cursor = conexao.cursor(dictionary=True)

    entrada = input("Digite o id do cliente que deseja editar: ").strip()

    if not entrada:
        print("Erro: o id não pode ficar em branco.")
        cursor.close()
        return

    try:
        id_cliente = int(entrada)
    except ValueError:
        print("Erro: digite um id válido.")
        cursor.close()
        return

    try:
        cursor.execute("SELECT * FROM clientes WHERE id = %s", (id_cliente,))
        cliente = cursor.fetchone()

        if not cliente:
            print("Cliente não encontrado")
            cursor.close()
            return

        novo_nome = input(f"Nome ({cliente['nome']}): ").strip()
        novo_endereco = input(f"Endereço ({cliente['endereco']}): ").strip()
        novo_email = input(f"Email ({cliente['email']}): ").strip()
        novo_telefone = input(f"Telefone ({cliente['telefone']}): ").strip()

        if novo_nome == "":
            novo_nome = cliente['nome']
        if novo_endereco == "":
            novo_endereco = cliente['endereco']
        if novo_email == "":
            novo_email = cliente['email']
        if novo_telefone == "":
            novo_telefone = cliente['telefone']

        sql = """
            UPDATE clientes
            SET nome = %s, endereco = %s, email = %s, telefone = %s
            WHERE id = %s
        """
        valores = (novo_nome, novo_endereco, novo_email, novo_telefone, id_cliente)

        cursor.execute(sql, valores)
        conexao.commit()
        print("Cliente atualizado com sucesso")
    except Exception as erro:
        print(f"Erro ao editar cliente: {erro}")

    cursor.close()