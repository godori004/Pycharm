import pandas as pd
import urllib3

INDEX = '<td class="num"><span class="tah p11">'

TODAY     = 5
YESTERDAY = 10


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
    a = a.replace('\\t', '')
    a = a.split('\n')

    for t2 in a:
        if t2.startswith(INDEX):
            value = int(t2.replace(INDEX,"")[0:-12].replace(",",""))
            break

    return value
