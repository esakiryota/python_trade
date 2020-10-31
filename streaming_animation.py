import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import random
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

fig = plt.figure()

xlim = [0,100]
X, Y = [], []

def plot(data):
    plt.cla()

    api = API(access_token=access_token, environment="practice")
    r = pricing.PricingInfo(accountID=accountID, params={'instruments': instruments})
    rv = api.request(r)

    Y.append(float(rv['prices'][0]['bids'][0]['price']))
    X.append(len(Y))

    if len(X) > 100:
        xlim[0]+=1
        xlim[1]+=1

    plt.plot(X, Y)
    plt.title("sample animation (real time)")
    y_max, y_min = max(Y)+(max(Y)-min(Y))*0.1, min(Y)-(max(Y)-min(Y))*0.1
    # plt.set_ylim((y_min, y_max))
    plt.ylim(y_min, y_max)
    plt.xlim(xlim[0],xlim[1])


# 10msごとにplot関数を呼び出してアニメーションを作成
ani = animation.FuncAnimation(fig, plot, interval=100)
#ani.save('sample2.gif', writer='imagemagick')
plt.show()
