def menu_funcionarios(conexao):
    while True:
        print("\n=== FUNCIONÁRIOS ===")
        print("1 - Cadastrar funcionário")
        print("2 - Ver todos os funcionários")
        print("3 - Editar funcionário")
        print("4 - Excluir funcionário")
        print("0 - Voltar")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            cadastrar_funcionario(conexao)
        elif opcao == "2":
            verfuncionarios(conexao)
        elif opcao == "3":
            editarfuncionario(conexao)
        elif opcao == "4":
            excluirfuncionario(conexao)
        elif opcao == "0":
            print("Voltando...")
            break
        else:
            print("Opção inválida!")


def cadastrar_funcionario(conexao):
    cursor = conexao.cursor(dictionary=True)

    nome = input("Nome: ").strip()
    cpf = input("CPF: ").strip()
    cargo = input("Cargo: ").strip()
    salario = input("Salário: ").strip()
    telefone = input("Telefone: ").strip()

    if not nome or not cpf or not cargo or not salario or not telefone:
        print("Erro: não deixe campo em branco.")
        cursor.close()
        return

    try:
        salario = float(salario)
    except ValueError:
        print("Erro: salário inválido.")
        cursor.close()
        return

    try:
        sql = """
            INSERT INTO funcionarios (nome, cpf, cargo, salario, telefone)
            VALUES (%s, %s, %s, %s, %s)
        """
        valores = (nome, cpf, cargo, salario, telefone)
        cursor.execute(sql, valores)
        conexao.commit()
        print(f"Funcionário {nome} cadastrado com sucesso")
    except Exception as erro:
        print(f"Erro ao cadastrar funcionário: {erro}")

    cursor.close()


def verfuncionarios(conexao):
    cursor = conexao.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM funcionarios")
        funcionarios = cursor.fetchall()

        if not funcionarios:
            print("Nenhum funcionário cadastrado.")
        else:
            for element in funcionarios:
                print(f"""
INFORMAÇÕES DO FUNCIONÁRIO {element['id']}
Nome: {element['nome']}
CPF: {element['cpf']}
Cargo: {element['cargo']}
Salário: {element['salario']}
Telefone: {element['telefone']}
""")
    except Exception as erro:
        print(f"Erro ao buscar funcionários: {erro}")

    cursor.close()


def excluirfuncionario(conexao):
    cursor = conexao.cursor(dictionary=True)

    entrada = input("Digite o id do funcionário que deseja excluir: ").strip()

    if not entrada:
        print("Erro: o id não pode ficar em branco.")
        cursor.close()
        return

    try:
        id_funcionario = int(entrada)
    except ValueError:
        print("Erro: digite um id válido.")
        cursor.close()
        return

    try:
        cursor.execute("DELETE FROM funcionarios WHERE id = %s", (id_funcionario,))
        conexao.commit()

        if cursor.rowcount > 0:
            print("Funcionário excluído com sucesso")
        else:
            print("Funcionário não encontrado")
    except Exception as erro:
        if "foreign key constraint fails" in str(erro).lower():
            print("Não é possível excluir este funcionário, pois ele ja tem uma venda registrada.")
        else:
            print(f"Erro ao excluir funcionário: {erro}")

    cursor.close()


def editarfuncionario(conexao):
    cursor = conexao.cursor(dictionary=True)

    entrada = input("Digite o id do funcionário que deseja editar: ").strip()

    if not entrada:
        print("Erro: o id não pode ficar em branco.")
        cursor.close()
        return

    try:
        id_funcionario = int(entrada)
    except ValueError:
        print("Erro: digite um id válido.")
        cursor.close()
        return

    try:
        cursor.execute("SELECT * FROM funcionarios WHERE id = %s", (id_funcionario,))
        funcionario = cursor.fetchone()

        if not funcionario:
            print("Funcionário não encontrado")
            cursor.close()
            return

        novo_nome = input(f"Nome ({funcionario['nome']}): ").strip()
        novo_cpf = input(f"CPF ({funcionario['cpf']}): ").strip()
        novo_cargo = input(f"Cargo ({funcionario['cargo']}): ").strip()
        novo_salario = input(f"Salário ({funcionario['salario']}): ").strip()
        novo_telefone = input(f"Telefone ({funcionario['telefone']}): ").strip()

        if novo_nome == "":
            novo_nome = funcionario['nome']
        if novo_cpf == "":
            novo_cpf = funcionario['cpf']
        if novo_cargo == "":
            novo_cargo = funcionario['cargo']
        if novo_salario == "":
            novo_salario = funcionario['salario']
        else:
            try:
                novo_salario = float(novo_salario)
            except ValueError:
                print("Erro: salário inválido.")
                cursor.close()
                return
        if novo_telefone == "":
            novo_telefone = funcionario['telefone']

        sql = """
            UPDATE funcionarios
            SET nome = %s, cpf = %s, cargo = %s, salario = %s, telefone = %s
            WHERE id = %s
        """
        valores = (novo_nome, novo_cpf, novo_cargo, novo_salario, novo_telefone, id_funcionario)

        cursor.execute(sql, valores)
        conexao.commit()
        print("Funcionário atualizado com sucesso")
    except Exception as erro:
        print(f"Erro ao editar funcionário: {erro}")

    cursor.close()