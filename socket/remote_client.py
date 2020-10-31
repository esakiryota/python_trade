import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://10.4.128.14:6789/")
num = 7
result = proxy.double()
print("Double %s is %s" % (num, result))
