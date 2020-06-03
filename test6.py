from src.stock import *
import time

sleepTime = 10  #틱

stockArr = myStockInfo.getMyStockObject()   #객체 생성

while True:
    for stockInfo in stockArr:
        tmp = "{} : {}|".format(stockInfo.name, stockInfo.getCurrentValueStr())
        print(tmp, end='')
    print()
    time.sleep(sleepTime)