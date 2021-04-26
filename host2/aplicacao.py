import xmlrpc.client

with xmlrpc.client.ServerProxy("http://localhost:8888/") as proxy:
    print(proxy.listar_arquivos())