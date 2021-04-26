import xmlrpc.client

with xmlrpc.client.ServerProxy("http://localhost:8100/") as proxy:
    print(proxy.listar_arquivos())