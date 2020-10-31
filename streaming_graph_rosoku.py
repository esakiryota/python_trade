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
import pandas as pd
import datetime
from matplotlib import animation

accountID = "101-009-16203168-001"
instruments = "EUR_USD"
access_token = '3b8cc5d4afd552fbae00ba3506cdf2c3-45285f64acd5b3eb972e62bd62f5905d'

data = []
tik_data = []
time = datetime.datetime.now()
time_5m = datetime.timedelta(minutes=5)

api = API(access_token=access_token, environment="practice")
r = pricing.PricingInfo(accountID=accountID, params={'instruments': instruments})
rv = api.request(r)

data.append( [
    rv['prices'][0]['time'][:19],
    float(rv['prices'][0]['bids'][0]['price']),
    float(rv['prices'][0]['bids'][0]['price']),
    float(rv['prices'][0]['bids'][0]['price']),
    float(rv['prices'][0]['bids'][0]['price']),
    float(rv['prices'][0]['bids'][0]['price'])
    ])
tik_data.append([
    rv['prices'][0]['time'][:19],
    float(rv['prices'][0]['bids'][0]['price'])
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

print(df)

sub_df = pd.DataFrame(tik_data)
sub_df.columns = ['Datetime', 'Price']
sub_df['Datetime'] = pd.to_datetime(sub_df['Datetime'])
sub_df['Price'] = sub_df["Price"].astype(float)
sub_df = sub_df.set_index('Datetime')

fig, axis = mpf.plot(df, returnfig=True,figsize=(11,8),type='candle',title='\n\nGrowing Candle')
ax = axis[0]

def append_df(price):
    global time
    global df
    df.loc[time] = price

def stream(price):
    global df
    global time
    print('編集')
    if (price > df.iloc[-1]['High']):
        df.iloc[-1]['High'] = price
    if (price < df.iloc[-1]['Low']):
        df.iloc[-1]['Low'] = price
    print('編集終了')


def main(data):
    global time
    global df
    global sub_df
    global time_5m
    api = API(access_token=access_token, environment="practice")
    r = pricing.PricingInfo(accountID=accountID, params={'instruments': instruments})
    rv = api.request(r)
    price = float(rv['prices'][0]['bids'][0]['price'])
    now = rv['prices'][0]['time'][:19]
    tik_data.append([
        now,
        price
        ])
    sub_df.loc[now] = price
    print(sub_df)
    if (time < datetime.datetime.now() and datetime.datetime.now() < time+time_5m) :
        print('stream')
        stream(price)
    else:
        time = time+time_5m
        print('initial')
        append_df(price)
    print('last')
    # ax.clear()
    mpf.plot(df, type='candle', volume=True, figratio=(12,4))
    print('finish')


ani = animation.FuncAnimation(fig, main, interval=2000)
mpf.show()
