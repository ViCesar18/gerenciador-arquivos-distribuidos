from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client
import os

def Union(lista1, lista2, lista3, lista4):
    lista = list(set().union(lista1, lista2, lista3, lista4))
    return lista


def listar_arquivos():
    files2 = []
    files3 = []
    files4 = []
    with xmlrpc.client.ServerProxy("http://localhost:8200/") as proxy:
        files2 = proxy.listar_arquivos()

    with xmlrpc.client.ServerProxy("http://localhost:8300/") as proxy:
        files3 = proxy.listar_arquivos()

    with xmlrpc.client.ServerProxy("http://localhost:8400/") as proxy:
        files4 = proxy.listar_arquivos()

    return Union(os.listdir("."), files2, files3, files4)


def criar_arquivo():
    return 0


def renomear_arquivo():
    return 0


def excluir_arquivo():
    return 0


server = SimpleXMLRPCServer(("localhost", 8100))
print("Escutando a porta 8100...")
server.register_function(listar_arquivos, "listar_arquivos")
server.serve_forever()