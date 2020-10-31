import zmq
import oandapyV20.endpoints.pricing as pricing
from oandapyV20 import API
import time
import requests

line_api = "https://notify-api.line.me/api/notify"
token = "wEXUd1PA13nFNL5zlSVd8Ipau5wBTSavxnUfRTyh3um"
headers = {"Authorization" : "Bearer "+ token}

accountID = "101-009-16203168-001"
instruments = "EUR_USD"
access_token = '3b8cc5d4afd552fbae00ba3506cdf2c3-45285f64acd5b3eb972e62bd62f5905d'
api = API(access_token=access_token, environment="practice")
r = pricing.PricingInfo(accountID=accountID, params={'instruments': instruments})

def start_server():
    context = zmq.Context()
    pub = context.socket(zmq.PUB)
    pub.bind("tcp://172.20.10.3:5556")

    print("Server startup.")

    for i in range(10):
        rv = api.request(r)
        message = i
        payload = {"message" :  message}
        post = requests.post(line_api, headers = headers, params=payload)
        time.sleep(1)
        print('Publish: %s' % i)

    # while True:
    #     # time.sleep(1)
    #     rv = api.request(r)
    #     price = 'あ'
    #     # price = rv['prices'][0]['bids'][0]['price']
    #     message = socket.recv_string()
    #     print("Received message = %s" % message)
    #     socket.send_string("Reply: %s" % message)
    #
    # socket.close()
    # context.destroy()

if __name__ == "__main__":
    start_server()
