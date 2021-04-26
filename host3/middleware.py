from xmlrpc.server import SimpleXMLRPCServer
import os

def listar_arquivos():
    return os.listdir(".")


def criar_arquivo():
    return 0


def renomear_arquivo():
    return 0


def excluir_arquivo():
    return 0


server = SimpleXMLRPCServer(("localhost", 8888))
print("Escutando a porta 8888...")
server.register_function(listar_arquivos, "listar_arquivos")
server.serve_forever()