import xmlrpc.client

def listar():
    with xmlrpc.client.ServerProxy("http://localhost:8100/") as proxy:
        print(proxy.listar_arquivos())

def renomear(nomeAntigo, nomeNovo):
    with xmlrpc.client.ServerProxy("http://localhost:8100/") as proxy:
        proxy.renomear_arquivo(nomeAntigo, nomeNovo)

while(True):
    linha = str(input(">")).split()
    comando = linha[0]
    if comando == "ls":
        listar()
    elif comando == "renomear":
        if len(linha) != 3:
            print("Devem ser fornecidos dois argumentos! (nomeAntigo, novoNome)")
        else:
            renomear(linha[1], linha[2])
    elif comando == "sair":
        break
    else:
        print("Comando invalido")
