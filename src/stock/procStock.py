from src.stock import naverInfo
from pandas import DataFrame


class ProcStock:
    def __init__(self, name, code, df):
        # stock 정보
        self.code = code
        self.name = name

        # naver 관련
        self.naverUrl = None
        self.naverArr = []

        # 내 정보
        self.myPrice = 0
        self.myStockCnt = 0
        self.price = 0

        self.dataFame = DataFrame({})

        # 거래
        self.toDayTradingVolume = 0
        self.yesTerTradingVolume = 0
        self.tradingVolumeAvg = 0

        # 초기화 메소드 실행
        self.initalize()

    # 변수 초기화 메소드
    def initalize(self):
        self.naverUrl = naverInfo.get_url(self.code)
        # self.naverArr = self.getNaverInfoArr()

    def setCode(self, code):
        self.code = code

    def setMyPrice(self, price):
        self.myPrice = price

    def getMyPrice(self):
        return self.myPrice

    def seMyStockCnt(self, cnt):
        self.myStockCnt = cnt

    def getCurrentValueStr(self):
        # 한번 더 호출 해야 갱신 된다.
        self.setNaverInfoArr()

        return self.naverArr[0]

    def getNaverInfoArr(self):
        return naverInfo.get_info_arr(self.naverUrl)

    def setNaverInfoArr(self):
        if self.naverUrl == None:
            raise Exception("naverUrl 호출 이 선행 되어야 합니다.")

        self.naverArr = self.getNaverInfoArr()

        return self.naverArr

    # Data Frame 으로 진행 할때 메소드
    def getDailyPrice(self):
        # print("코드[{0}]".format(self.code))
        self.dataFame = naverInfo.get_price_to_dataFrame(self.naverUrl).dropna()

    # naver 관련 메소드
    def getCurrentValue(self):
        self.getDailyPrice()
        return self.dataFame.head(1).get("종가")[1]

    # Data Frame 으로 진행 할때 메소드



