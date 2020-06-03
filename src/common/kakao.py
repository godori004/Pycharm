import urllib3

def getCode():
    #GET /oauth/authorize?client_id={app_key}&redirect_uri=http://test&response_type=code HTTP/1.1
    #Host: kauth.kakao.com

    restKey = 'ec35680abe2bc3a507a0bb672c4fabfb'

    http = urllib3.PoolManager()

    url = 'https://kauth.kakao.com/oauth/authorize'

    r = http.request('GET',url, fields={'client_id':restKey,'redirect_uri':'https://www.naver.com','response_type':'code'})

    #호출 url
    #https://kauth.kakao.com/oauth/authorize?client_id=ec35680abe2bc3a507a0bb672c4fabfb&redirect_uri=https%3A%2F%2Fwww.naver.com&response_type=code
    #로그인 진행 하면 코드를 준다
    # 받은 코드 20200403
    #XSKNxeIxoB8KGyPskS2Z2h-BcunvYgPga5EUY88hISKbK9rMrdAY4lKJGTo_vXlwJ4uqJgo9cxcAAAFxPmUcng

def getToken():

    restKey = 'ec35680abe2bc3a507a0bb672c4fabfb'
    code = 'dky8NZUBTHLTaFZDCSdJmwvZ-Hs2Ll6WaDF5TqlLLxJxsl8kpy7tyEfvLpE7akS0mXO4FAorDNQAAAFxTI_4eQ'

    http = urllib3.PoolManager()

    url = 'https://kauth.kakao.com/oauth/token'

    r = http.request('GET', url,
                     fields={'grant_type': 'authorization_code', 'client_id': restKey, 'redirect_uri':'https://www.naver.com', 'code': code})

    print(r.data.decode())