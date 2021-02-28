import json
import requests
import setting


setting = setting.load()
print(setting)

API_BASE = "https://api.vrchat.cloud/api/1"

url = "{}/config".format(API_BASE)

#ここを微調整するといい感じになるよ
response = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'})
apiKey = json.loads(response.text)["clientApiKey"]
print(apiKey)

# 
from requests.auth import HTTPBasicAuth
# なるほど　ここをしゃかしゃか動かせばOK
USER     = setting['MAIL']
PASSWORD = setting['PASS']

url = "{}/auth/user".format(API_BASE)
response = requests.get(url, params={"apiKey": apiKey},auth=HTTPBasicAuth(USER, PASSWORD),headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'})
print(response)
# token = json.loads(response.text)["authToken"] # "authcookie_[UUID]" みたいなのが返ってくる
token = response.cookies["auth"] # (API変更のためCookieからauthTokenを取得、2018/7/8追記)

# フレンド一覧
url = "{}/auth/user/friends".format(API_BASE)
response = requests.get(url, params={"apiKey": apiKey, "authToken": token},headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'})
friends = json.loads(response.text)
for f in friends:
    print(f)
    print(f["displayName"]) # オンラインなフレンド一覧を表示

##############################
# なるほどー
f = friends[0]
url = "{}/user/{}/friendStatus".format(API_BASE,f['id'])
response = requests.get(url, params={"apiKey": apiKey, "authToken": token},headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15'})
print(url)
friends = json.loads(response.text)
print(friends)
####################################
