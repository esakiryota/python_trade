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
# instrument = "EUR_USD"
access_token = '3b8cc5d4afd552fbae00ba3506cdf2c3-45285f64acd5b3eb972e62bd62f5905d'
api = API(access_token=access_token, environment="practice")
r = pricing.PricingInfo(accountID=accountID, params={'instruments': "EUR_USD"})


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

def getCandleDataFromOanda(instrument, api, date_from, date_to, granularity):
    params = {
        "from": date_from.isoformat(),
        "to": date_to.isoformat(),
        "granularity": granularity,
    }
    r = instruments.InstrumentsCandles(instrument=instrument, params=params)
    return api.request(r)

all_data = []
#2020年7月の10分足
date_from = datetime.datetime(2020, 11, 3)
date_to = datetime.datetime.now() + datetime.timedelta(hours=-14)
# date_to = datetime.datetime.now()
print(date_to)
ret = getCandleDataFromOanda("EUR_USD", api, date_from, date_to, "M5")

data = []
for res in ret['candles']:
    data.append( [
        res['time'][:19],
        res['volume'],
        float(res['mid']['o']),
        float(res['mid']['h']),
        float(res['mid']['l']),
        float(res['mid']['c']),
        ])

rs = df.resample(resample_period).agg(resample_map).dropna()

for i in range(len(data)):
    now = pd.to_datetime(data[i][0])
    sr_data = pd.Series([data[i][2], data[i][5], data[i][3], data[i][4], data[i][1]], index=['Open', 'Close', 'High', 'Low', 'Volume'], name=now)
    df = df.append(sr_data)

# rs.append(data)

rtorder = trade_order.RealTimeOrder()

rs_length = 0

def main():
    global df
    global rs
    global rtorder
    global rs_length
    nxt = rtapi.next()
    df = df.append(nxt)
    rs = df.resample(resample_period).agg(resample_map).dropna()
    old_rs_length = rs_length
    rs_length = len(rs)
    print(old_rs_length)
    print(rs_length)
    df["SMA1"] = df['Open'].rolling(10).mean()
    df["SMA2"] = df['Open'].rolling(50).mean()
    df["Position"] = np.where(df["SMA1"] > df["SMA2"] , 1 , -1)
    df["Returns"] = np.log(df["Open"] / df["Open"].shift(1))
    df["Strategy"] = df["Position"].shift(1) * df["Returns"]
    rs["SMA1"] = rs['Open'].rolling(10).mean()
    rs["SMA2"] = rs['Open'].rolling(50).mean()
    rs["Position"] = np.where(rs["SMA1"] > rs["SMA2"] , 1 , -1)
    rs["Returns"] = np.log(rs["Open"] / rs["Open"].shift(1))
    rs["Strategy"] = rs["Position"].shift(1) * rs["Returns"]
    print(rs.iloc[-1, -3])
    print(rs.iloc[-2, -3])
    if old_rs_length < rs_length:
        if rs.iloc[-1, -3] == -1 and rs.iloc[-2, -3] == 1:
            rtorder.tradeCreateOrder()
        elif rs.iloc[-1, -3] == 1 and rs.iloc[-2, -3] == -1:
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
