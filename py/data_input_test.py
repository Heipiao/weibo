#coding=utf-8
from weibo import APIClient
from kafka import KafkaProducer

import json
import time

APP_KEY = "3722673574"
APP_SECRET = "3686fea0a65da883b6c2a7586f350425"
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'     
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)

with open('token.json', 'r') as f:
    r = json.load(f)
access_token = r["access_token"]
expires_in = r["expires_at"]
client.set_access_token(access_token, expires_in)
producer = KafkaProducer()

# put data into kafka
def put_data_kafka():
    raw_data  = client.statuses.public_timeline.get()
    for x in range(0,len(raw_data)):
    	print raw_data.statuses[1].text.encode("utf-8") 
        text = raw_data.statuses[1].text.encode("utf-8")
        producer.send('test',text)
        producer.flush()

# aviod the too-fast
def control_pace():
	i = 1
    while i <= 50:
        put_data_kafka()
        i += 1
        time.sleep(10) # sleep 10 seconds

control_pace()
