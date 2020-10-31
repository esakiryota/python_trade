from xmlrpc.server import SimpleXMLRPCServer
import requests

def double():
    line_api = "https://notify-api.line.me/api/notify"
    token = "wEXUd1PA13nFNL5zlSVd8Ipau5wBTSavxnUfRTyh3um"
    headers = {"Authorization" : "Bearer "+ token}
    message = 'hi'
    payload = {"message" :  message}
    post = requests.post(line_api, headers = headers, params=payload)

server = SimpleXMLRPCServer(("10.4.128.14", 6789))
server.register_function(double, "double")
server.serve_forever()
