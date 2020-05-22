from stock import naverInfo
from pandas import DataFrame

class ProcStock:
    def __init__(self, code):

        self.myPrice            = 0
        self.myStockCnt         = 0
        self.price              = 0
        self.code               = code
        self.dataFame           = DataFrame({})
        self.tradingVolume      = 0
        self.tradingVolumeAvg   = 0


    def setCode(self, code):
        self.code = code

    def setMyPrice(self, price):
        self.myPrice = price

    def getMyPrice(self):
        return self.myPrice

    def seMyStockCnt(self, cnt):
        self.myStockCnt = cnt

    def getDailyPrice(self):
        #print("코드[{0}]".format(self.code))
        self.dataFame = naverInfo.get_price_to_dataFrame(naverInfo.get_url(self.code)).dropna()

    def getCurrentValue(self):
        self.getDailyPrice()
        return self.dataFame.head(1).get("종가")[1]

    def getCurrentValueStr(self):
        return naverInfo.get_price_to_str(naverInfo.get_url(self.code))



