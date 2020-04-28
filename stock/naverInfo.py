import pandas as pd

def get_url(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    get_url(code)

def get_url(code_df):
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code_df)

    print("요청 URL = {}".format(url))
    return url

def get_price(url):
    df = pd.DataFrame();  # 결과 받아올 데이터 프레임
    for page in range(1, 5):
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

    return df