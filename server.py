from xmlrpc.server import SimpleXMLRPCServer
import os

def buscar_ips():
    print(server.address_family)

server = SimpleXMLRPCServer(("0.0.0.0", 8000))
print("Escutando a porta 8000...")
server.register_function(buscar_ips, "buscar_ips")
server.serve_forever()