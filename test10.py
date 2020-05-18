import urllib3
import re
from datetime import datetime
from stock import naverInfo

http = urllib3.PoolManager()

req = http.request('GET', "http://finance.naver.com/item/sise_day.nhn?code=005430")
a = str(req.data)
count = 0
date = ""
value = 0

a = a.replace('\\n', '\n')
a = a.replace('\\t', '\t')
t = a.split('\n')

#pattern = re.compile("\\t\\t\\t\\t\\t")

date = datetime.today().strftime('%Y.%m.%d')
pattern = re.compile(".+."+date)

for t2 in t:
    m = pattern.match(t2)
    if m:
        count=count+1
    else:
        if count==1:
            value = t2.split(">")[2].split("<")[0].replace(",","")
            print(t2.split(">")[2].split("<")[0].replace(",",""))
            break





#r = http.request('GET',url, headers={'Authorization':'Bearer Ih7NfdTTvFbW7xxFQSLEf5qSeKSdLNyMzBKmVQo9dVoAAAFxPtCllA'})