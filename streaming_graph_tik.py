import json
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.pricing import PricingStream
from oandapyV20 import API
import oandapyV20.endpoints.pricing as pricing
import time
import requests
import matplotlib.pyplot as plt
import numpy as np
import mplfinance as mpf

accountID = "101-009-16203168-001"
instruments = "EUR_USD"
access_token = '3b8cc5d4afd552fbae00ba3506cdf2c3-45285f64acd5b3eb972e62bd62f5905d'


fig, ax = plt.subplots(1, 1)
x = []
y = []

lines, = ax.plot(x, y)

for i in range(0, 100, 1):
    api = API(access_token=access_token, environment="practice")
    r = pricing.PricingInfo(accountID=accountID, params={'instruments': instruments})
    rv = api.request(r)
    y.append(float(rv['prices'][0]['bids'][0]['price']))
    x.append(rv['prices'][0]['time'])
    y_max, y_min = max(y)+(max(y)-min(y))*0.1, min(y)-(max(y)-min(y))*0.1
    ax.set_ylim((y_min, y_max))
    ax.plot(x, y, color='blue')
    plt.pause(1)
    print(rv['prices'][0]['bids'][0]['price'])
    print(i, "秒経過")
