from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import shutil
import os
import time
    
arquivo_ocupado = False


def retorna_arquivo_ocupado():
    if arquivo_ocupado:
        return 1
    
    return 0


def exclusao_mutua():
    n_arquivos_ocupados = 1

    print("Entrou na exclusao")
    while n_arquivos_ocupados != 0:
        n_arquivos_ocupados = 0
        for middle_addr in MIDDLE_LIST:
            with xmlrpc.client.ServerProxy(middle_addr) as proxy:
                n_arquivos_ocupados += proxy.retorna_arquivo_ocupado()

    print("Saiu da exclusao")


def listar_arquivos_middle():
    return os.listdir("./dir")


def listar_arquivos():
    arquivos = []

    exclusao_mutua()

    for middle_addr in MIDDLE_LIST:
        with xmlrpc.client.ServerProxy(middle_addr) as proxy:
            arquivos += proxy.listar_arquivos_middle()

    return list(set().union(listar_arquivos_middle(), arquivos))


def buscar_tamanho_diretorio():
    tamanho = 0
    
    for dirpath, dirnames, filenames in os.walk("./dir"):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            tamanho += os.path.getsize(fp)
    
    return tamanho


def criar_arquivo_middle(nome_arquivo):
    arquivo = os.path.join("../arquivos_para_criar", nome_arquivo)
    shutil.copy(arquivo, "./dir")


def criar_arquivo(nome_arquivo):
    exclusao_mutua()

    lista_tamanhos = [{
        "middle_addr": "",
        "tamanho": buscar_tamanho_diretorio()
    }]

    for middle_addr in MIDDLE_LIST:
        with xmlrpc.client.ServerProxy(middle_addr) as proxy:
            lista_tamanhos.append({
                "middle_addr": middle_addr,
                "tamanho": proxy.buscar_tamanho_diretorio()
            })

    lista_tamanhos = sorted(lista_tamanhos, key = lambda i: i["tamanho"])

    for i in range(2):
        if lista_tamanhos[i]["middle_addr"] == "":
            criar_arquivo_middle(nome_arquivo)
        else:
            with xmlrpc.client.ServerProxy(lista_tamanhos[i]["middle_addr"]) as proxy:
                proxy.criar_arquivo_middle(nome_arquivo)


def renomear_arquivo_middle(nome_antigo, nome_novo):
    arquivo_antigo = os.path.join("./dir", nome_antigo)
    arquivo_novo = os.path.join("./dir", nome_novo)
    os.rename(arquivo_antigo, arquivo_novo)


def renomear_arquivo(nome_antigo, nome_novo):
    exclusao_mutua()

    arquivo_ocupado = True

    for file in listar_arquivos_middle():
        if file == nome_antigo:
            renomear_arquivo_middle(nome_antigo, nome_novo)

    for middle_addr in MIDDLE_LIST:
        with xmlrpc.client.ServerProxy(middle_addr) as proxy:
            files = proxy.listar_arquivos_middle()

            for file in files:
                if file == nome_antigo:
                    proxy.renomear_arquivo_middle(nome_antigo, nome_novo)

    time.sleep(60)

    arquivo_ocupado = False


def excluir_arquivo_middle(nome_arquivo):
    arquivo = os.path.join("./dir", nome_arquivo)
    os.remove(arquivo)


def excluir_arquivo(nome_arquivo):
    exclusao_mutua()

    arquivo_ocupado = True

    for file in listar_arquivos_middle():
        if file == nome_arquivo:
            excluir_arquivo_middle(nome_arquivo)

    for middle_addr in MIDDLE_LIST:
        with xmlrpc.client.ServerProxy(middle_addr) as proxy:
            files = proxy.listar_arquivos_middle()

            for file in files:
                if file == nome_arquivo:
                    proxy.excluir_arquivo_middle(nome_arquivo)

    arquivo_ocupado = False


BLUE_YELLOW   = "\033[1;33;44m"  
RED  = "\033[1;31m"
CYAN  = "\033[1;36m"
GREEN = "\033[1;32m"
END_COLOR = "\033[m"

""" print(BLUE_YELLOW + "Forneca o IP:PORT deste Middleware ->\n" + END_COLOR)
IP = input(CYAN + "IP Deste Middleware -> " + END_COLOR)
PORT = int(input(CYAN + "Porta Deste Middleware -> " + END_COLOR))

print(BLUE_YELLOW + "\nFornaca o IP:PORT dos outros Middlewares com o Formato IP:PORTA ->" + END_COLOR)
print(GREEN + "Exemplo -> 127.0.0.1:8000\n" + END_COLOR)
addr1 = input(CYAN + "Middleware 1 -> " + END_COLOR)
addr2 = input(CYAN + "Middleware 2 -> " + END_COLOR)
addr3 = input(CYAN + "Middleware 3 -> " + END_COLOR) """

""" MIDDLEWARE_1 = "http://" + addr1
MIDDLEWARE_2 = "http://" + addr2
MIDDLEWARE_3 = "http://" + addr3 """

MIDDLEWARE_1 = "http://localhost:8100"
MIDDLEWARE_2 = "http://localhost:8200"
MIDDLEWARE_3 = "http://localhost:8400"

MIDDLE_LIST = [MIDDLEWARE_1, MIDDLEWARE_2, MIDDLEWARE_3]

server = SimpleXMLRPCServer(("localhost", 8300), allow_none=True)
print(RED + f"\nEscutando a porta {8300}..." + END_COLOR)

server.register_function(retorna_arquivo_ocupado, "retorna_arquivo_ocupado")
server.register_function(listar_arquivos, "listar_arquivos")
server.register_function(listar_arquivos_middle, "listar_arquivos_middle")
server.register_function(buscar_tamanho_diretorio, "buscar_tamanho_diretorio")
server.register_function(criar_arquivo, "criar_arquivo")
server.register_function(criar_arquivo_middle, "criar_arquivo_middle")
server.register_function(renomear_arquivo, "renomear_arquivo")
server.register_function(renomear_arquivo_middle, "renomear_arquivo_middle")
server.register_function(excluir_arquivo, "excluir_arquivo")
server.register_function(excluir_arquivo_middle, "excluir_arquivo_middle")
server.serve_forever()
