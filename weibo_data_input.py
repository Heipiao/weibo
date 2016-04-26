
# -*- coding: utf-8 -*-  
#/usr/bin/env python  
 
#access to SinaWeibo By sinaweibopy 
#实现微博自动登录，token自动生成，保存及更新 
#适合于后端服务调用 
  

from weibo import APIClient  
import pymongo  
import sys, os, urllib, urllib2  
from http_helper import *  
from retry import *  
try:  
    import json  
except ImportError:  
    import simplejson as json  
  
# setting sys encoding to utf-8  
default_encoding = 'utf-8'  
if sys.getdefaultencoding() != default_encoding:  
    reload(sys)  
    sys.setdefaultencoding(default_encoding)  
  
# weibo api访问配置  
APP_KEY = '3722673574'      # app key  
APP_SECRET = '7a6de53498caf87e655a98fa2f8912bf'   # app secret  
REDIRECT_URL = 'https://api.weibo.com/oauth2/default.html' # callback url 授权回调页,与OAuth2.0 授权设置的一致  
USERID = '15029357121'       # 登陆的微博用户名，必须是OAuth2.0 设置的测试账号                     
USERPASSWD = 'liu8315'   # 用户密码  
 
  
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=REDIRECT_URL)  
  
def make_access_token():  
    #请求access token  
    params = urllib.urlencode({
        'action':'submit',
        'withOfficalFlag':'0',
        'ticket':'',
        'isLoginSina':'',  
        'response_type':'code',
        'regCallback':'',
        'redirect_uri':REDIRECT_URL,
        'client_id':APP_KEY,
        'state':'',
        'from':'',
        'userId':USERID,
        'passwd':USERPASSWD,
        })  
  
    login_url = 'https://api.weibo.com/oauth2/authorize'  
  
    url = client.get_authorize_url()  
    content = urllib2.urlopen(url)  
    if content:  
        headers = { 'Referer' : url }  
        request = urllib2.Request(login_url, params, headers)  
        opener = get_opener(False)  
        urllib2.install_opener(opener)  
        try:  
            f = opener.open(request)  
            return_redirect_uri = f.url                
        except urllib2.HTTPError, e:  
            return_redirect_uri = e.geturl()  
        # 取到返回的code  
        code = return_redirect_uri.split('=')[1]  
    #得到token  
    token = client.request_access_token(code,REDIRECT_URL)  
    print token
    save_access_token(token)  
  
def save_access_token(token):  
    #将access token保存到MongoDB数据库
    mongoCon=pymongo.Connection(host="127.0.0.1",port=27017)
    db= mongoCon.weibo
   
    t={
               "access_token":token['access_token'],
               "expires_in":str(token['expires_in']),
               "date":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
               }
    db.token.insert(t,safe=True)  

#Decorator 目的是当调用make_access_token()后再执行一次apply_access_token()
@retry(1)  
def apply_access_token():  
    #从MongoDB读取及设置access token 
    try:  

        mongoCon=pymongo.Connection(host="127.0.0.1",port=27017)
        db= mongoCon.weibo
        if db.token.count()>0:
            tokenInfos=db.token.find().sort([("_id",pymongo.DESCENDING)]).limit(1)
        else:  
            make_access_token()  
            return False  

        for  tokenInfo in tokenInfos:
            access_token=tokenInfo["access_token"]
            expires_in=tokenInfo["expires_in"]
        
        try:  
            client.set_access_token(access_token, expires_in)  
        except StandardError, e:  
            if hasattr(e, 'error'):   
                if e.error == 'expired_token':  
                    # token过期重新生成  
                    make_access_token()
                    return False  
            else:  
                pass  
    except:  
        make_access_token()
        return False  
      
    return True  
  
if __name__ == "__main__":  
    make_access_token()  
  
    # 以下为访问微博api的应用逻辑  
    # 以发布文字微博接口为例
    client.statuses.update.post(status='Test OAuth 2.0 Send a Weibo!')