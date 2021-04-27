import xmlrpc.client

def listar():
    with xmlrpc.client.ServerProxy(MIDDLE_ADDR) as proxy:
        arquivos = proxy.listar_arquivos()

        if arquivos != None:
            print()
            for nome_arquivo in arquivos:
                print(YELLOW + nome_arquivo + END_COLOR)
            print()


def renomear(nome_antigo, nome_novo):
    with xmlrpc.client.ServerProxy(MIDDLE_ADDR) as proxy:
        proxy.renomear_arquivo(nome_antigo, nome_novo)


def excluir(nome_arquivo):
    with xmlrpc.client.ServerProxy(MIDDLE_ADDR) as proxy:
        proxy.excluir_arquivo(nome_arquivo)


def criar(nome_arquivo):
    with xmlrpc.client.ServerProxy(MIDDLE_ADDR) as proxy:
        proxy.criar_arquivo(nome_arquivo)


BLUE_YELLOW   = "\033[1;33;44m"  
CYAN  = "\033[1;36m"
YELLOW = "\033[0;33m"
END_COLOR = "\033[m"

print(BLUE_YELLOW + "Forneca o IP:PORT do Middleware referente a esta Aplicação ->\n" + END_COLOR)
IP = input(CYAN + "IP Deste Middleware -> " + END_COLOR)
PORT = int(input(CYAN + "Porta Deste Middleware -> " + END_COLOR))

MIDDLE_ADDR = f"http://{IP}:{PORT}"

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
