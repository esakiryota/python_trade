from oandapyV20 import API
import oandapy
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.pricing import PricingStream
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.instruments as instruments
import json
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
from itertools import product


accountID = "101-009-16203168-001"
access_token = '3b8cc5d4afd552fbae00ba3506cdf2c3-45285f64acd5b3eb972e62bd62f5905d'

api = API(access_token=access_token, environment="practice")

def getCandleDataFromOanda(instrument, api, date_from, date_to, granularity):
    params = {
        "from": date_from.isoformat(),
        "to": date_to.isoformat(),
        "granularity": granularity,
    }
    r = instruments.InstrumentsCandles(instrument=instrument, params=params)
    return api.request(r)
#
# def stringToDatetime(datetimestring):
#
#
#

all_data = []
#2020年7月の10分足
date_from = datetime.datetime(2020, 8, 1)
date_to = datetime.datetime(2020, 8, 31)
# date_to = date_from + relativedelta(months=+1, day=1)
ret = getCandleDataFromOanda("USD_JPY", api, date_from, date_to, "M10")

data = []
for res in ret['candles']:
    data.append( [
        res['time'][:19],
        res['volume'],
        res['mid']['o'],
        res['mid']['h'],
        res['mid']['l'],
        res['mid']['c'],
        ])

df = pd.DataFrame(data)
df.columns = ['Datetime', 'Volume', 'Open', 'High', 'Low', 'Close']
df['Datetime'] = pd.to_datetime(df['Datetime'])
df['Volume'] = df["Volume"].astype(float)
df['Open'] = df["Open"].astype(float)
df['High'] = df["High"].astype(float)
df['Low'] = df["Low"].astype(float)
df['Close'] = df["Close"].astype(float)
df = df.set_index('Datetime')

SMA1 = 10
SMA2 = 50

df["SMA1"] = df['Open'].rolling(SMA1).mean()
df["SMA2"] = df['Open'].rolling(SMA2).mean()

data = df[["SMA1", "SMA2"]].dropna()

# df.drop('Volume', axis=1).plot()
df[["SMA1", "SMA2"]].plot()

df["Position"] = np.where(df["SMA1"] > df["SMA2"] , 1 , -1)
df["Returns"] = np.log(df["Open"] / df["Open"].shift(1))
df["Strategy"] = df["Position"].shift(1) * df["Returns"]
ax = df[["Returns", "Strategy"]].cumsum().apply(np.exp).plot()
df['Position'].plot(ax=ax, secondary_y='Position', style='--')

plt.show()

sma1 = range(1, 11, 1)
sma2 = range(10, 111, 10)

def sma12adjusting(sma1, sma2):
    result = pd.DataFrame()

    for SMA1, SMA2 in product(sma1, sma2):
        data = pd.DataFrame(df["Open"])
        data.dropna(inplace=True)
        data["Returns"] = np.log(data["Open"] / data["Open"].shift(1))
        data["SMA1"] = data['Open'].rolling(SMA1).mean()
        data["SMA2"] = data['Open'].rolling(SMA2).mean()
        data.dropna(inplace=True)
        data["Position"] = np.where(data["SMA1"] > data["SMA2"] , 1 , -1)
        data["Strategy"] = data["Position"].shift(1) * data["Returns"]
        data.dropna(inplace=True)
        pref = np.exp(df[["Returns", "Strategy"]].sum())
        result = result.append(pd.DataFrame(
        {'SMA1': SMA1, 'SMA2': SMA2, 'MARKET': pref['Returns'], 'STRATEGY': pref['Strategy'], 'OUT': pref['Returns'] - pref['Strategy']}, index=[0]
        ), ignore_index=True)

    print(result.sort_values('OUT', ascending=False).head(7))

sma12adjusting(sma1, sma2)
