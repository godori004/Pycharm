import urllib3
import json
from common import kakao

accessToken='PCeOZm56toA1Y568FyYbQPgt2ioe2FFHmUdGIAopyNkAAAFxTJMq_Q';
#Ih7NfdTTvFbW7xxFQSLEf5qSeKSdLNyMzBKmVQo9dVoAAAFxPtCllA

template_object = dict({'object_type': "text",
        'text': "헬로 헬로111",
        'link': {
            'web_url': "https://developers.kakao.com",
            'mobile_web_url': "https://developers.kakao.com"
        },
        'button_title': "바로 확인"
    })


http = urllib3.PoolManager()

url = 'https://kapi.kakao.com/v1/api/talk/friends'
#r = http.request('GET',url, headers={'Authorization':'Bearer Ih7NfdTTvFbW7xxFQSLEf5qSeKSdLNyMzBKmVQo9dVoAAAFxPtCllA'})

#rData = r.data.decode('UTF-8')

#print(rData)

template_object=str(json.dumps(template_object))
print(template_object)

url = 'https://kapi.kakao.com/v2/api/talk/memo/default/send'
r = http.request('POST', url, headers={'Authorization':'Bearer '+accessToken, 'Content-Type': 'application/x-www-form-urlencoded'}
                            , body='template_object=' + template_object
                 )

rData = r.data.decode('UTF-8')

print(rData)

#print(kakao.getToken())
#{"access_token":"Ih7NfdTTvFbW7xxFQSLEf5qSeKSdLNyMzBKmVQo9dVoAAAFxPtCllA","token_type":"bearer","refresh_token":"-KYU-MmbhNf5pI5Xn-fzCG413GJ1DY-HbVgGLwo9dVoAAAFxPtClkw","expires_in":21599,"scope":"story_read talk_message profile story_publish friends","refresh_token_expires_in":5183999}
