import json
from oandapyV20.endpoints.orders import OrderCreate
from oandapyV20.endpoints.trades import TradeDetails, TradeClose
from oandapyV20.endpoints.positions import OpenPositions, PositionClose
from oandapyV20 import API
import requests
import time

account_id = "101-009-16203168-001"
access_token = '3b8cc5d4afd552fbae00ba3506cdf2c3-45285f64acd5b3eb972e62bd62f5905d'

api = API(access_token=access_token, environment="practice")

# ids = []

class RealTimeOrder():
    def __init__(self):
        self.ids = []
        self.api = "https://notify-api.line.me/api/notify"
        self.token = "wEXUd1PA13nFNL5zlSVd8Ipau5wBTSavxnUfRTyh3um"
        self.headers = {"Authorization" : "Bearer "+ self.token}


    def tradeCreateOrder(self):
        data = {
            "order": {
                "instrument": "USD_JPY",
                "units": 10000,
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }
        ep = OrderCreate(accountID=account_id, data=data)
        rsp = api.request(ep)
        print(json.dumps(rsp["lastTransactionID"]))
        print("成り行き注文")
        self.ids.append(rsp["lastTransactionID"])
        message = '成り行き注文'
        payload = {"message" :  message}
        post = requests.post(self.api, headers = self.headers, params=payload)

    def tradeOrderClose(self):
        data = None
        for id in self.ids:
            ep = TradeClose(accountID=account_id, tradeID=id, data=data)
            rsp = api.request(ep)
            print(json.dumps(rsp, indent=2))
            message = 'トレード決済実行'
            payload = {"message" :  message}
            post = requests.post(self.api, headers = self.headers, params=payload)
            self.ids.remove(id)

    def tradeOrderInfo(self):
        ep = OpenPositions(accountID=account_id)
        rsp = api.request(ep)
        print(json.dumps(rsp, indent=2))
        if not rsp["positions"]:
            print("positionはありません")
            return
        else:
            for id in rsp["positions"][0]["long"]["tradeIDs"]:
                self.ids.append(id)

# rtorder = RealTimeOrder()
#
# rtorder.tradeOrderInfo()
# time.sleep(5)
# rtorder.tradeOrderClose()





# tradeCreateOrder()
# positionID = tradeOrderInfo()
# tradeOrderClose(positionID)

# data = None
# print("②トレード決済実行")
# ep = TradeClose(accountID=accountID, tradeID=trade_id, data=data)
# rsp = api.request(ep)
# print(json.dumps(rsp, indent=2))
# print("①オープン中の全ポジション情報を取得（決済前）")
# ep = OpenPositions(accountID=accountID)
# rsp = api.request(ep)
# print(json.dumps(rsp, indent=2))
# data = {
#     "longUnits": "ALL",
#     "shortUnits": "ALL"
# }
#
# print("②ポジションをクローズ")
# ep = PositionClose(accountID=accountID, instrument="USD_JPY", data=data)
# rsp = api.request(ep)
# print(json.dumps(rsp, indent=2))
