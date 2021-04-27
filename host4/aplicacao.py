import xmlrpc.client

def listar():
    with xmlrpc.client.ServerProxy("http://localhost:8100/") as proxy:
        print(proxy.listar_arquivos())


def renomear(nome_antigo, nome_novo):
    with xmlrpc.client.ServerProxy("http://localhost:8100/") as proxy:
        proxy.renomear_arquivo(nome_antigo, nome_novo)


def excluir(nome_arquivo):
    with xmlrpc.client.ServerProxy("http://localhost:8100/") as proxy:
        proxy.excluir_arquivo(nome_arquivo)


def criar(nome_arquivo):
    with xmlrpc.client.ServerProxy("http://localhost:8100/") as proxy:
        proxy.criar_arquivo(nome_arquivo)


while(True):
    linha = str(input(">")).split()
    comando = linha[0]
    if comando == "ls":
        listar()
    elif comando == "criar":
        if len(linha) != 2:
            print("Devem ser fornecidos dois argumentos! (nome_arquivo)")
        else:
            criar(linha[1])
    elif comando == "renomear":
        if len(linha) != 3:
            print("Devem ser fornecidos dois argumentos! (nome_antigo, nome_novo)")
        else:
            renomear(linha[1], linha[2])
    elif comando == "excluir":
        if len(linha) != 2:
            print("Deve ser fornecido um argumento! (nome_arquivo)")
        else:
            excluir(linha[1])
    elif comando == "sair":
        break
    else:
        print("Comando invalido")
