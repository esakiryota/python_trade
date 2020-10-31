import json
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import numpy as np
from itertools import product
from sklearn.linear_model import LinearRegression

raw = pd.read_csv('data/SP500_NOV2019_IDay.csv', index_col=0, parse_dates=True)

data = pd.DataFrame(raw['Open'])

data['returns'] = np.log(data/data.shift(1))
data.dropna(inplace=True)
data['direction'] = np.sign(data['returns']).astype(int)

print(data.head())
lags = 2

def create_lags(data):
    global cols
    cols = []
    for lag in range(1, lags + 1):
        col = 'lags_{}'.format(lag)
        data[col] = data['returns'].shift(lag)
        cols.append(col)

create_lags(data)

data.dropna(inplace=True)

model = LinearRegression()

data['pos_ols_1'] = model.fit(data[cols], data['returns']).predict(data[cols])
data['pos_ols_2'] = model.fit(data[cols], data['direction']).predict(data[cols])

print(data[['pos_ols_1', 'pos_ols_2']].head())

data[['pos_ols_1', 'pos_ols_2']] = np.where(data[['pos_ols_1', 'pos_ols_2']] > 0, 1, -1)

data['strat_ols_1'] = data['pos_ols_1'] * data['returns']
data['strat_ols_2'] = data['pos_ols_2'] * data['returns']

print(data[['returns', 'strat_ols_1', 'strat_ols_2']].sum().apply(np.exp))
print((data['direction'] == data['pos_ols_1']).value_counts())

data[['returns', 'strat_ols_1', 'strat_ols_2']].cumsum().apply(np.exp).plot(figsize=(10, 6))

plt.show()






# print(data.head())
