import urllib3
import re
from datetime import datetime, timedelta
from stock import naverInfo

http = urllib3.PoolManager()

INDEX='<td class="num"><span class="tah p11">'

VOLUME = 5

req = http.request('GET', "http://finance.naver.com/item/sise_day.nhn?code=900340")
a = str(req.data)

count = 1
date = ""
value = 0

a = a.replace('\\n', '\n')
a = a.replace('\\t', '')
t = a.split('\n')

naverArr = []

#pattern = re.compile("\\t\\t\\t\\t\\t")

date = datetime.today().strftime('%Y.%m.%d')
pattern = re.compile(".+."+date)

#print(datetime.today()-timedelta(1))

for t2 in t:
    if t2.startswith(INDEX):
        naverArr.append(int(t2.replace(INDEX,"")[0:-12].replace(",","")))

for t2 in naverArr:

    volume = "거래량"
    value = "가격"

    if count%5==0:
        print(volume, end="")
    else:
        print(value, end="")
    print(t2)
    count=count+1

#for t2 in t:
#    m = pattern.match(t2)
#    if m:
#        count=count+1
#    else:
#        if count==1:
#            value = t2.split(">")[2].split("<")[0].replace(",","")
#            print(t2.split(">")[2].split("<")[0].replace(",",""))
#            break





#r = http.request('GET',url, headers={'Authorization':'Bearer Ih7NfdTTvFbW7xxFQSLEf5qSeKSdLNyMzBKmVQo9dVoAAAFxPtCllA'})