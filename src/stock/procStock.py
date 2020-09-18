from src.stock import naverInfo
from pandas import DataFrame


class ProcStock:
    def __init__(self, name, code):

        self.CUR_VALUE = 0
        self.TODAY_VOLUME = 4
        self.YESTERDAY_VOLUME = 9

        # stock 정보
        self.code = code
        self.name = name
        self.curVolume = 0
        self.beforVolume = 0

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
        return self.naverArr[self.CUR_VALUE]

    def isBeforVolumeOver(self):
        if (self.naverArr[self.TODAY_VOLUME] - self.naverArr[self.YESTERDAY_VOLUME]) > 0:
            return "거"
        else:
            return ""

    def getYesterTodayRatio(self):
        ratio = self.naverArr[self.TODAY_VOLUME] / self.naverArr[self.YESTERDAY_VOLUME] * 100
        return int(ratio)

    def getCurBeforValueRate(self):

        rate = 0

        self.curVolume = self.naverArr[self.TODAY_VOLUME]

        if self.beforVolume > 0:
            rate = int((self.curVolume / self.beforVolume) * 100)

        print("{} : {} : {}".format(self.code, self.curVolume, self.beforVolume))

        self.beforVolume = self.naverArr[self.TODAY_VOLUME]

        return rate

    def getCurVolumn(self):

        valumn = 0

        self.curVolume = self.naverArr[self.TODAY_VOLUME]

        if self.beforVolume > 0:
            valumn = int(self.curVolume - self.beforVolume)

        self.beforVolume = self.naverArr[self.TODAY_VOLUME]

        return valumn

    def getNaverInfoArr(self):
        return naverInfo.get_info_arr(self.naverUrl)

    def setNaverInfoArr(self):
        if self.naverUrl is None:
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



