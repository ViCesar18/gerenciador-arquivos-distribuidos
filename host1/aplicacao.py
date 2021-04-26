import xmlrpc.client

def listar():
    with xmlrpc.client.ServerProxy("http://localhost:8100/") as proxy:
        print(proxy.listar_arquivos())

while(True):
    comando = str(input(">"))
    if(comando == "ls"):
        listar()
    elif(comando == "sair"):
        break
    else:
        print("Comando invalido")