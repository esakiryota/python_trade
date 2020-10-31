import json
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.pricing import PricingStream
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
import time
import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

accountID = "101-009-16203168-001"
instruments = "EUR_USD"
access_token = '3b8cc5d4afd552fbae00ba3506cdf2c3-45285f64acd5b3eb972e62bd62f5905d'

s = PricingStream(accountID=accountID, params={"instruments":instruments})
api = API(access_token=access_token, environment="practice")
MAXREC = 10

fig, ax = plt.subplots(1, 1)
info = []

try:
    n = 0
    for R in api.request(s):
        print(json.dumps(R, indent=2))
        if ("bids" in R.keys()):
            cols = ['Datetime', 'bids','asks', 'closeoutBid', 'closeoutAsk', 'instrument']
            df = pd.DataFrame(index= [], columns=cols)
            info.append([
            R["time"][:19],
            R["bids"][0]["price"],
            R["asks"][0]["price"],
            R["closeoutBid"],
            R["closeoutAsk"],
            R["instrument"]
            ])
            df = pd.DataFrame(info)
            df.columns = cols
            df['Datetime'] = pd.to_datetime(df['Datetime'])
            df = df.set_index('Datetime')
            print(json.dumps(R["bids"][0]["price"], indent=2))
            print(df)
        n += 1
        if n > MAXREC:
            s.terminate("maxrecs received {}".format(MAXREC))

except V20Error as e:
    print("Error: {}".format(e))
