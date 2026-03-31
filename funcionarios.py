def menu_funcionarios(conexao):
    while True:
        print("\n=== FUNCIONÁRIOS ===")
        print("1 - Cadastrar funcionário")
        print("2 - Ver todos os funcionários")
        print("3 - Editar funcionário")
        print("4 - Excluir funcionário")
        print("0 - Voltar")

        opcao = input("Escolha: ")

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
    nome = input("Nome: ")
    cpf = input("CPF: ")
    cargo = input("Cargo: ")
    salario = input("Salário: ")
    telefone = input("Telefone: ")

    cursor.execute(f"""
        INSERT INTO funcionarios (nome, cpf, cargo, salario, telefone)
        VALUES ('{nome}', '{cpf}', '{cargo}', '{salario}', '{telefone}')
    """)
    conexao.commit()
    cursor.close()
    print(f"Funcionário {nome} cadastrado com sucesso")

def verfuncionarios(conexao):
    cursor = conexao.cursor(dictionary=True)
    cursor.execute('SELECT * FROM funcionarios')
    for element in cursor.fetchall():
        print(f"""
        INFORMAÇÕES DO FUNCIONÁRIO {element['id']}
        Nome: {element['nome']}
        CPF: {element['cpf']}
        Cargo: {element['cargo']}
        Salário: {element['salario']}
        Telefone: {element['telefone']}
    """)
    cursor.close()

def excluirfuncionario(conexao):
    cursor = conexao.cursor(dictionary=True)
    id = int(input("Digite o id do funcionário que deseja excluir: "))
    cursor.execute(f"DELETE FROM funcionarios WHERE id = {id}")
    conexao.commit()
    cursor.close()
    print("Funcionário excluído com sucesso")

def editarfuncionario(conexao):
    cursor = conexao.cursor(dictionary=True)
    id = int(input("Digite o id do funcionário que deseja editar: "))
    
    cursor.execute(f"SELECT * FROM funcionarios WHERE id = {id}")
    funcionario = cursor.fetchone()
    
    if funcionario:
        novo_nome = input(f"Nome ({funcionario['nome']}): ") 
        novo_cpf = input(f"CPF ({funcionario['cpf']}): ") 
        novo_cargo = input(f"Cargo ({funcionario['cargo']}): ") 
        novo_salario = input(f"Salário ({funcionario['salario']}): ") 
        novo_telefone = input(f"Telefone ({funcionario['telefone']}): ") 


        cursor.execute(f"""
            UPDATE funcionarios
            SET nome = '{novo_nome}', cpf = '{novo_cpf}', cargo = '{novo_cargo}', salario = '{novo_salario}', telefone = '{novo_telefone}'
            WHERE id = {id}
        """)
        conexao.commit()
        print("Funcionário atualizado com sucesso")
    else:
        print("Funcionário não encontrado")

    cursor.close()