from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os

def Union(lista1, lista2, lista3, lista4):
    lista = list(set().union(lista1, lista2, lista3, lista4))
    return lista
    

def listar_arquivos_middle():
    return os.listdir(".")


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

    return Union(os.listdir("."), files1, files2, files3)


def criar_arquivo():
    return 0


def renomear_arquivo_middle(nomeAntigo, novoNome):
    os.rename(nomeAntigo, novoNome)

def renomear_arquivo():
    return 0


def excluir_arquivo():
    return 0


server = SimpleXMLRPCServer(("0.0.0.0", 8300), allow_none=True)
print("Escutando a porta 8300...")
server.register_function(listar_arquivos, "listar_arquivos")
server.register_function(listar_arquivos_middle, "listar_arquivos_middle")
server.register_function(renomear_arquivo, "renomear_arquivo")
server.register_function(renomear_arquivo_middle, "renomear_arquivo_middle")
server.serve_forever()