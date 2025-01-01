import numpy as np

#note:Not tool optimal, made following university assignment recomendations
#nota:Não otimizado com relação ao uso de ferramentas, feito com base nas regras de entrega da universidade

def le_dados():
    inventario = np.genfromtxt(r"C:\Users\erice\OneDrive\Área de Trabalho\planilhas\inventario.csv", dtype=np.int32,
                               skip_header=1, delimiter=",")
    operacoes = np.genfromtxt(r"C:\Users\erice\OneDrive\Área de Trabalho\planilhas\operacoes.csv", dtype=np.int32,
                              skip_header=1, delimiter=",")
    clientes = np.genfromtxt(r"C:\Users\erice\OneDrive\Área de Trabalho\planilhas\clientes.csv", dtype='U40',
                             skip_header=1, delimiter=",")
    lojas = np.genfromtxt(r"C:\Users\erice\OneDrive\Área de Trabalho\planilhas\lojas.csv", dtype='U40',
                          skip_header=1, delimiter=",")
    produtos = np.genfromtxt(r"C:\Users\erice\OneDrive\Área de Trabalho\planilhas\produtos.csv", dtype='U40',
                             skip_header=1, delimiter=",")
    return inventario, operacoes, clientes, lojas, produtos

def preco_item(inventario, id_loja, id_produto):
    for item in inventario:
        if item[0] == id_loja:
            if item[1] == id_produto:
                return item[2]

def nome_loja(lojas, id_loja):
    for loja in lojas:
        if loja[0] == str(id_loja):
            return loja[1]

def nome_produto(produtos, id_produto):
    for produto in produtos:
        if produto[0] == str(id_produto):
            return produto[1]

def nome_cliente(clientes, id_cliente):
    for cliente in clientes:
        if cliente[0] == str(id_cliente):
            return cliente[1]

def remove_estoque(inventario, id_loja, id_produto, quantidade):
    for item in inventario:
        if item[0] == id_loja:
            if item[1] == id_produto:
                item[3] = item[3] - quantidade

def soma_caixa(lojas, id_loja, valor):
    for loja in lojas:
        if loja[0] == str(id_loja):
            loja[2] = int(loja[2]) + valor

def atualiza_estoques(inventario, operacoes):
    i = 0
    while i < len(operacoes):
        oper = operacoes[i]
        id_cliente, id_loja, id_produto, quantidade = oper       
        j = 0
        while j < quantidade:
            remove_estoque(inventario, id_loja, id_produto, 1)
            j = j + 1        
        i = i + 1
    print(inventario, id_loja, id_produto)


def atualiza_caixas(inventario, lojas, operacoes):
    i = 0
    while i < len(operacoes):
        oper = operacoes[i]
        id_cliente, id_loja, id_produto, quantidade = oper       
        if preco_item(inventario, id_loja, id_produto) > 0:
            valor = preco_item(inventario, id_loja, id_produto) * quantidade
            j = 0
            while j < quantidade:
                j = j + 1     
        i = i + 1
    print(inventario, id_loja, id_produto)
    np.savetxt("_lojas_.csv", lojas, "%s", delimiter=",", header="id_loja,nome_loja,caixa")

def vendas_por_produto(operacoes, produtos):
    nprodutos = produtos.shape[0]
    vendas = np.zeros([nprodutos, 2], dtype=np.int32)
    for i in range(nprodutos):
        vendas[i,0] = produtos[i,0]
    nops = operacoes.shape[0]
    for i in range(nops):
        id_cliente, id_loja, id_produto, quantidade = operacoes[i]
        for j in range(nprodutos):
            if vendas[j,0] == id_produto:
                vendas[j,1] += quantidade
    return vendas

def quantidade_vendidos(vendas, id_produto):
    i = 0
    while i < len(vendas):
        if vendas[i][0] == id_produto:
            return vendas[i][1]
        i = i + 1
    j = 0
    while j < len(vendas):
        if vendas[j][0] == id_produto:
            return vendas[j][1]
        j = j + 1

def reposicao(inventario, operacoes, produtos):
    vendas = vendas_por_produto(operacoes, produtos)
    rep = []
    i = 0
    while i < len(inventario):
        id_loja, id_produto, quantidade = inventario[i][0], inventario[i][1], inventario[i][3]
        if quantidade != 0:
            rep.append([id_loja, id_produto, 0])
        else:
            j = 0
            while j < len(vendas):
                if vendas[j][0] == id_produto:
                    quantidade_repor = 1 + vendas[j][1] // 2
                    rep.append([id_loja, id_produto, quantidade_repor])
                    break
                j = j + 1
        i = i + 1  
    rep = np.array(rep, dtype=np.int32)
    np.savetxt("_estoque_.csv", rep, "%d", delimiter=",", header="id_loja,id_produto,quantidade")
    return rep

def faturamento_por_loja(inventario, operacoes, lojas):
    faturamentos = np.zeros((lojas.shape[0], 2), dtype=np.int32)
    i = 0
    while i < lojas.shape[0]:
        loja = lojas[i]
        faturamentos[i, 0] = int(loja[0])
        i = i + 1   
    j = 0
    while j < len(operacoes):
        operacao = operacoes[j]
        id_cliente, id_loja, id_produto, quantidade = operacao
        preco = preco_item(inventario, id_loja, id_produto)
        if preco != 0:
            valor = preco * quantidade
            l = 0
            while l < faturamentos.shape[0]:
                if faturamentos[l, 0] == id_loja:
                    faturamentos[l, 1] = faturamentos[l, 1] + valor
                    break
                l = l + 1
        j = j + 1
    return faturamentos

def relatorio_lojas(inventario, operacoes, lojas):
    faturamentos = faturamento_por_loja(inventario, operacoes, lojas)
    nlojas = lojas.shape[0]
    for i in range(nlojas):
        id_loja = faturamentos[i,0]
        valor = faturamentos[i,1]
        loja = nome_loja(lojas, id_loja)
        if valor > 0:
            print(f'A loja "{loja}" faturou R${valor}')
        else:
            print(f'A loja "{loja}" não teve vendas')

def gasto_por_cliente(inventario, operacoes, clientes):
    gastos = np.zeros((clientes.shape[0], 2), dtype=np.int32)
    i = 0
    while i < clientes.shape[0]:
        cliente = clientes[i]
        gastos[i, 0] = int(cliente[0])
        i = i + 1
    j = 0
    while j < len(operacoes):
        operacao = operacoes[j]
        id_cliente, id_loja, id_produto, quantidade = operacao
        preco = preco_item(inventario, id_loja, id_produto)
        if preco != 0:
            valor = preco * quantidade
            l = 0
            while l < gastos.shape[0]:
                if gastos[l, 0] == id_cliente:
                    gastos[l, 1] = gastos[l, 1] + valor
                    break
                l = l + 1
        j = j + 1
    return gastos

def relatorios_individuais(inventario, operacoes, clientes, lojas):
    gastos = gasto_por_cliente(inventario, operacoes, clientes)
    nclientes = gastos.shape[0]
    clientes_ativos = []
    faturamento = 0
    for i in range(nclientes):
        if gastos[i,1] > 0:
            id_cliente = gastos[i,0]
            gasto = gastos[i,1]
            cliente = nome_cliente(clientes, id_cliente)
            faturamento += gasto
            clientes_ativos.append(cliente)
            print(f"{cliente} gastou no total R${gasto}")
    return faturamento, clientes_ativos

def relatorio_clientes(inventario, operacoes, clientes, lojas):
    faturamento, clientes_ativos = relatorios_individuais(inventario, operacoes, clientes, lojas)

    if len(clientes_ativos) == 0:
        print("Nenhum cliente fez compras no shopping hoje!")
        return

    nomes = ', '.join(clientes_ativos)
    ultima_virgula = nomes.rfind(", ")
    nomes = (nomes[:ultima_virgula] + " e " + nomes[ultima_virgula +2:])
    print(f"{len(clientes_ativos)} clientes fizeram compras no shopping:",
          nomes)
    media = faturamento / len(clientes_ativos)
    print(f"Os clientes gastaram em média R${media:.2f}")
    print(f"O faturamento total do shopping foi R${faturamento}")

def relatorio_estoques(reposicoes, lojas, produtos):
    nitems = reposicoes.shape[0]
    for i in range(nitems):
        id_loja, id_produto, quantidade = reposicoes[i]
        if quantidade > 0:
            loja = nome_loja(lojas, id_loja)
            produto = nome_produto(produtos, id_produto)
            print(f'A loja "{loja}" deve comprar {quantidade} 'f'unidades do produto {produto}')

inventario, operacoes, clientes, lojas, produtos=le_dados()
atualiza_caixas(inventario,lojas,operacoes)