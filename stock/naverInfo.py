import pandas as pd
import urllib3
import re

from datetime import datetime

def get_url(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    get_url(code)

def get_url(code_df):
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code_df)
    #print("요청 URL = {}".format(url))
    return url

def get_price_to_dataFrame(url):
    df = pd.DataFrame();  # 결과 받아올 데이터 프레임
    for page in range(1, 5):
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

    return df

def get_price_to_str(url):

    count = 0
    date = ""
    value = 0

    http = urllib3.PoolManager()
    req = http.request('GET', url)
    a = str(req.data)

    a = a.replace('\\n', '\n')
    a = a.replace('\\t', '\t')
    t = a.split('\n')

    date = datetime.today().strftime('%Y.%m.%d')
    pattern = re.compile(".+." + date)

    for t2 in t:
        m = pattern.match(t2)
        if m:
            count = count + 1
        else:
            if count == 1:
                value = t2.split(">")[2].split("<")[0].replace(",", "")
                #print(t2.split(">")[2].split("<")[0].replace(",", ""))
                break

    return value