from oandapyV20 import API
from oandapyV20.exceptions import V20Error
from oandapyV20.endpoints.pricing import PricingStream
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.accounts as accounts
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
access_token = 'b2a7c2aa6b68ef25c93aad03947c3bfb-697e5f816749b897832415695d23e29e'

api = API(access_token=access_token, environment="practice")

params = { "instruments": "EUR_USD,EUR_JPY,USD_JPY" }

params = {
  "count": 5,
  "granularity": "M5"
}
data =  {
    "order": {
        "price": "1.17934",
        "stopLossOnFill": {
            "timeInForce": "GTC",
            "price": "1.17"
        },
        "side" : "buy",
        "instrument": "EUR_USD",
        "units": "100",
        "type": "MARKET",
        "positionFill": "DEFAULT"
    }
}
r = orders.OrderCreate(accountID, data=data)
api.request(r)
print(api.request(r))
