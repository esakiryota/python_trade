import pandas as pd
import mplfinance as mpf
import matplotlib.animation as animation
from oandapyV20.endpoints.pricing import PricingStream
import oandapyV20.endpoints.pricing as pricing
from oandapyV20 import API
import datetime

## Class to simulate getting more data from API:

accountID = "101-009-16203168-001"
instruments = "EUR_USD"
access_token = '3b8cc5d4afd552fbae00ba3506cdf2c3-45285f64acd5b3eb972e62bd62f5905d'
api = API(access_token=access_token, environment="practice")
r = pricing.PricingInfo(accountID=accountID, params={'instruments': instruments})


class RealTimeAPI():
    def __init__(self):
        self.data_pointer = 0
        # self.data_frame = pd.read_csv('data/to_csv_out.csv',index_col=0,parse_dates=True)
        rv = api.request(r)
        price = float(rv['prices'][0]['bids'][0]['price'])
        now = rv['prices'][0]['time'][:19]
        data = []
        for i in range(10):
            data.append([now, '0', price, price, price, price])
        self.data_frame = pd.DataFrame(data)
        self.data_frame.columns = ['Datetime', 'Volume', 'Open', 'High', 'Low', 'Close']
        self.data_frame['Datetime'] = pd.to_datetime(self.data_frame['Datetime'])
        self.data_frame = self.data_frame.set_index('Datetime')
        self.df_len = len(self.data_frame)

    def fetch_next(self):
        # r1 = self.data_pointer
        # self.data_pointer += 1
        # if self.data_pointer >= self.df_len:
        #     return None
        rv = api.request(r)
        price = float(rv['prices'][0]['bids'][0]['price'])
        now = rv['prices'][0]['time'][:19]
        now = pd.to_datetime(now)
        data = pd.Series([price, price, price, price, '0'], index=['Open', 'Close', 'High', 'Low', 'Volume'], name=now)
        print(data)
        # return self.data_frame.iloc[r1:self.data_pointer,:]
        return data

    def initial_fetch(self):
        # if self.data_pointer > 0:
        #     return
        # r1 = self.data_pointer
        # self.data_pointer += int(0.2*self.df_len)
        # return self.data_frame.iloc[r1:self.data_pointer,:]
        return self.data_frame

rtapi = RealTimeAPI()

resample_map ={'Open' :'first',
               'High' :'max'  ,
               'Low'  :'min'  ,
               'Close':'last' }
resample_period = '5T'

df = rtapi.initial_fetch()
rs = df.resample(resample_period).agg(resample_map).dropna()

print(df.head())
print(rs.head())



fig, axes = mpf.plot(rs,returnfig=True,figsize=(11,8),type='candle',title='\n\nGrowing Candle')
ax = axes[0]

print(ax)

def animate(ival):
    global df
    global rs
    nxt = rtapi.fetch_next()
    if nxt is None:
        print('no more data to plot')
        ani.event_source.interval *= 3
        if ani.event_source.interval > 12000:
            exit()
        return
    df = df.append(nxt)
    rs = df.resample(resample_period).agg(resample_map).dropna()
    # xmin = datetime.datetime.strptime(sxmin, '%Y-%m-%d')
    # xmax = datetime.datetime.strptime(sxmax, '%Y-%m-%d')
    # mpf.xlim([xmin,xmax])
    ax.clear()
    mpf.plot(rs,ax=ax,type='candle')

ani = animation.FuncAnimation(fig, animate, interval=500)

mpf.show()
