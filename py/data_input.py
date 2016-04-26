#coding=utf-8
from weibo import APIClient
import json

APP_KEY = "3722673574"
APP_SECRET = "3686fea0a65da883b6c2a7586f350425"
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'     
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

with open('token.json', 'r') as f:
    r = json.load(f)
access_token = r["access_token"]
expires_in = r["expires_at"]
client.set_access_token(access_token, expires_in)
raw_data  = client.statuses.public_timeline.get()
print raw_data.statuses[1].text.encode("utf-8") 
