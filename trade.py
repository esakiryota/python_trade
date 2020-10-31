from oandapyV20 import API
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.pricing import PricingStream
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.accounts as accounts
import time
import oandapyV20.endpoints.pricing as pricing
import numpy as np
import trade_order
# import oandapy
# import pandas as pd
# import datetime
# from datetime import datetime, timedelta
# import pytz
# # API接続設定のファイルを読み込む
# import configparser

import json
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta


accountID = "101-009-16203168-001"
instruments = "EUR_USD"
access_token = '3b8cc5d4afd552fbae00ba3506cdf2c3-45285f64acd5b3eb972e62bd62f5905d'
api = API(access_token=access_token, environment="practice")
r = pricing.PricingInfo(accountID=accountID, params={'instruments': instruments})


class RealTimeData():
    def __init__(self):
        rv = api.request(r)
        price = float(rv['prices'][0]['bids'][0]['price'])
        now = rv['prices'][0]['time'][:19]
        data_array = []
        data_array.append([now, '0', price, price, price, price])
        self.data_frame = pd.DataFrame(data_array)
        self.data_frame.columns = ['Datetime', 'Volume', 'Open', 'High', 'Low', 'Close']
        self.data_frame['Datetime'] = pd.to_datetime(self.data_frame['Datetime'])
        self.data_frame = self.data_frame.set_index('Datetime')

    def next(self):
        rv = api.request(r)
        price = float(rv['prices'][0]['bids'][0]['price'])
        now = rv['prices'][0]['time'][:19]
        now = pd.to_datetime(now)
        data = pd.Series([price, price, price, price, '0'], index=['Open', 'Close', 'High', 'Low', 'Volume'], name=now)
        return data

    def initial(self):
        return self.data_frame

rtapi = RealTimeData()

resample_map ={'Open' :'first',
               'High' :'max'  ,
               'Low'  :'min'  ,
               'Close':'last' }
resample_period = '5T'

df = rtapi.initial()
rs = df.resample(resample_period).agg(resample_map).dropna()

rtorder = trade_order.RealTimeOrder()

def main():
    global df
    global rs
    global rtorder
    nxt = rtapi.next()
    df = df.append(nxt)
    rs = df.resample(resample_period).agg(resample_map).dropna()
    df["SMA1"] = df['Open'].rolling(10).mean()
    df["SMA2"] = df['Open'].rolling(50).mean()
    df["Position"] = np.where(df["SMA1"] > df["SMA2"] , 1 , -1)
    df["Returns"] = np.log(df["Open"] / df["Open"].shift(1))
    df["Strategy"] = df["Position"].shift(1) * df["Returns"]
    print(df.iloc[-1, -3])
    print(df.iloc[-2, -3])
    if df.iloc[-1, -3] == -1 and df.iloc[-2, -3] == 1:
        rtorder.tradeCreateOrder()
    elif df.iloc[-1, -3] == 1 and df.iloc[-2, -3] == -1:
        rtorder.tradeOrderClose()

while True:
    main()
    print(df.tail(3))
    print(rs.tail(3))
    time.sleep(1)


# params = {
#   "count": 5,
#   "granularity": "M5"
# }
# data =  {
#     "order": {
#         "price": "1.17934",
#         "stopLossOnFill": {
#             "timeInForce": "GTC",
#             "price": "1.17"
#         },
#         "side" : "buy",
#         "instrument": "EUR_USD",
#         "units": "100",
#         "type": "MARKET",
#         "positionFill": "DEFAULT"
#     }
# }
# r = orders.OrderCreate(accountID, data=data)
# api.request(r)
# print(api.request(r))
