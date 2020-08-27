from oandapyV20 import API
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.pricing import PricingStream
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.instruments as instruments
import json
import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt


accountID = "101-009-16203168-001"
access_token = 'b2a7c2aa6b68ef25c93aad03947c3bfb-697e5f816749b897832415695d23e29e'

api = API(access_token=access_token, environment="practice")

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
date_from = datetime.datetime(2020, 7, 1)
date_to = date_from + relativedelta(months=+1, day=1)
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
x = df["Datetime"].astype(str).values
y = df["High"].astype(float).values

plt.plot(y)
plt.show()
# print(df.head(10))
