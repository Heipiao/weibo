from weibo import Client
from pprint import pprint
from time import clock
import json

APP_KEY = "3722673574"
APP_SECTER = "3686fea0a65da883b6c2a7586f350425"
CALLBACK_URL = 'http://siliang.org'
code = "004ba6f4d40736d7aff25f4203d46f73"

c = Client(APP_KEY, APP_SECTER , CALLBACK_URL)
# url = c.authorize_url
# webbrowser.open_new(url)
c.set_code('code')
token = c.token
c = Client(APP_KEY, APP_SECTER , CALLBACK_URL,token)

#pprint(raw_data['statuses'][1]['text'])

a = []
raw_data  = c.get('statuses/public_timeline', count=200)
for x in range(200):
    a = a.append(str(raw_data['statuses'][x]['text']))

print (a)