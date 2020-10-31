import sys
import zmq
import oandapyV20.endpoints.pricing as pricing
from oandapyV20 import API
import time

accountID = "101-009-16203168-001"
instruments = "EUR_USD"
access_token = '3b8cc5d4afd552fbae00ba3506cdf2c3-45285f64acd5b3eb972e62bd62f5905d'
api = API(access_token=access_token, environment="practice")
r = pricing.PricingInfo(accountID=accountID, params={'instruments': instruments})

def start_client():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://172.20.10.3:5556")

    while True:
        # print("Enter message:")
        # message = sys.stdin.readline()
        time.sleep(1)
        rv = api.request(r)
        price = rv['prices'][0]['bids'][0]['price']
        socket.send_string(price)

        recv_message = socket.recv_string()
        print("Receive message = %s" % recv_message)

    socket.close()
    context.destroy()

if __name__ == "__main__":
    start_client()
