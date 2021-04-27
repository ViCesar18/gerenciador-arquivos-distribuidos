from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import shutil
import os

def Union(lista1, lista2, lista3, lista4):
    lista = list(set().union(lista1, lista2, lista3, lista4))
    return lista
    

def listar_arquivos_middle():
    return os.listdir("./dir")


def listar_arquivos():
    arquivos = []

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
    for file in listar_arquivos_middle():
        if file == nome_antigo:
            renomear_arquivo_middle(nome_antigo, nome_novo)

    for middle_addr in MIDDLE_LIST:
        with xmlrpc.client.ServerProxy(middle_addr) as proxy:
            files = proxy.listar_arquivos_middle()

            for file in files:
                if file == nome_antigo:
                    proxy.renomear_arquivo_middle(nome_antigo, nome_novo)


def excluir_arquivo_middle(nome_arquivo):
    arquivo = os.path.join("./dir", nome_arquivo)
    os.remove(arquivo)


def excluir_arquivo(nome_arquivo):
    for file in listar_arquivos_middle():
        if file == nome_arquivo:
            excluir_arquivo_middle(nome_arquivo)

    for middle_addr in MIDDLE_LIST:
        with xmlrpc.client.ServerProxy(middle_addr) as proxy:
            files = proxy.listar_arquivos_middle()

            for file in files:
                if file == nome_arquivo:
                    proxy.excluir_arquivo_middle(nome_arquivo)


print("Forneca o IP:PORT deste Middleware ->\n")
IP = input("IP Deste Middleware -> ")
PORT = int(input("Porta Deste Middleware -> "))

print("\nFornaca o IP:PORT dos outros Middlewares com o Formato IP:PORTA ->")
print("Exemplo -> 127.0.0.1:8000\n")
addr1 = input("Middleware 1 -> ")
addr2 = input("Middleware 2 -> ")
addr3 = input("Middleware 3 -> ")

MIDDLEWARE_1 = "http://" + addr1
MIDDLEWARE_2 = "http://" + addr2
MIDDLEWARE_3 = "http://" + addr3

MIDDLE_LIST = [MIDDLEWARE_1, MIDDLEWARE_2, MIDDLEWARE_3]

server = SimpleXMLRPCServer((IP, PORT), allow_none=True)
print(f"Escutando a porta {PORT}...")
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
