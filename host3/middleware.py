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
    files1 = []
    files2 = []
    files3 = []
    with xmlrpc.client.ServerProxy("http://localhost:8100/") as proxy:
        files2 = proxy.listar_arquivos_middle()

    with xmlrpc.client.ServerProxy("http://localhost:8200/") as proxy:
        files3 = proxy.listar_arquivos_middle()

    with xmlrpc.client.ServerProxy("http://localhost:8400/") as proxy:
        files3 = proxy.listar_arquivos_middle()

    return Union(os.listdir("./dir"), files1, files2, files3)


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
    tamanho1 = buscar_tamanho_diretorio()
    tamanho2 = 0
    tamanho3 = 0
    tamanho4 = 0

    with xmlrpc.client.ServerProxy("http://localhost:8100/") as proxy:
        tamanho2 = proxy.buscar_tamanho_diretorio()

    with xmlrpc.client.ServerProxy("http://localhost:8200/") as proxy:
        tamanho3 = proxy.buscar_tamanho_diretorio()

    with xmlrpc.client.ServerProxy("http://localhost:8400/") as proxy:
        tamanho4 = proxy.buscar_tamanho_diretorio()

    lista_tamanhos = [tamanho1, tamanho2, tamanho3, tamanho4]
    maior_tamanho = max(lista_tamanhos)

    if tamanho1 == maior_tamanho:
        lista_tamanhos.remove(maior_tamanho)
        criar_arquivo_middle(nome_arquivo)
        
        segundo_tamanho_max = max(lista_tamanhos)
        if tamanho2 == segundo_tamanho_max:
            with xmlrpc.client.ServerProxy("http://localhost:8100/") as proxy:
                tamanho2 = proxy.criar_arquivo_middle(nome_arquivo) 


def renomear_arquivo_middle(nome_antigo, nome_novo):
    arquivo_antigo = os.path.join("./dir", nome_antigo)
    arquivo_novo = os.path.join("./dir", nome_novo)
    os.rename(arquivo_antigo, arquivo_novo)


def renomear_arquivo(nome_antigo, nome_novo):
    for file in listar_arquivos_middle():
        if file == nome_antigo:
            renomear_arquivo_middle(nome_antigo, nome_novo)

    with xmlrpc.client.ServerProxy("http://localhost:8100/") as proxy:
        files = proxy.listar_arquivos_middle()

        for file in files:
            if file == nome_antigo:
                proxy.renomear_arquivo_middle(nome_antigo, nome_novo)

    with xmlrpc.client.ServerProxy("http://localhost:8200/") as proxy:
        files = proxy.listar_arquivos_middle()

        for file in files:
            if file == nome_antigo:
                proxy.renomear_arquivo_middle(nome_antigo, nome_novo)

    with xmlrpc.client.ServerProxy("http://localhost:8400/") as proxy:
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

    with xmlrpc.client.ServerProxy("http://localhost:8100/") as proxy:
        files = proxy.listar_arquivos_middle()

        for file in files:
            if file == nome_arquivo:
                proxy.excluir_arquivo_middle(nome_arquivo)

    with xmlrpc.client.ServerProxy("http://localhost:8200/") as proxy:
        files = proxy.listar_arquivos_middle()

        for file in files:
            if file == nome_arquivo:
                proxy.excluir_arquivo_middle(nome_arquivo)

    with xmlrpc.client.ServerProxy("http://localhost:8400/") as proxy:
        files = proxy.listar_arquivos_middle()

        for file in files:
            if file == nome_arquivo:
                proxy.excluir_arquivo_middle(nome_arquivo)


server = SimpleXMLRPCServer(("0.0.0.0", 8300), allow_none=True)
print("Escutando a porta 8300...")
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