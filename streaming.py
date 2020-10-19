import json
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.pricing import PricingStream
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
import time
import requests

accountID = "101-009-16203168-001"
instruments = "EUR_USD"
access_token = '3b8cc5d4afd552fbae00ba3506cdf2c3-45285f64acd5b3eb972e62bd62f5905d'

s = PricingStream(accountID=accountID, params={"instruments":instruments})
api = API(access_token=access_token, environment="practice")
MAXREC = 10

try:
    n = 0
    for R in api.request(s):
        print(json.dumps(R, indent=2))
        n += 1
        if n > MAXREC:
            s.terminate("maxrecs received {}".format(MAXREC))
except V20Error as e:
    print("Error: {}".format(e))

for i in range(0, 100, 1):
    api = API(access_token=access_token, environment="practice")
    r = pricing.PricingInfo(accountID=accountID, params={'instruments': instruments})
    rv = api.request(r)
    print(rv['prices'][0]['bids'])
    time.sleep(1)
    print(i, "秒経過")
