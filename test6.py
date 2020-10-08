from src.stock import *
import time

sleepTime = 10  #틱

stockArr = myStockInfo.getMyStockObject()   #객체 생성

while True:
    cnt = 1
    print()
    for stockInfo in stockArr:
        tmp = "{}:{}{}:{};{}|".format(stockInfo.name, stockInfo.getCurrentValueStr(), stockInfo.isBeforVolumeOver()
                                     , stockInfo.getCurVolumn(), stockInfo.getYesterTodayRatio())
        print(tmp, end='')
        #if (cnt % 5) == 0:
        #    print()

        cnt = cnt + 1
    print()
    time.sleep(sleepTime)

    #002900