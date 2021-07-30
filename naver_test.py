#-*- coding: utf-8 -*-
import os
import sys
import urllib.request
import json
import time
from urllib.error import HTTPError, URLError


def naver_api(search_key, search_count, client_id, client_secret, path):
    body = urllib.parse.quote(search_key)
    url = "https://openapi.naver.com/v1/search/image?query=" + body + "&display=" + str(search_count)

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    request.add_header("Content-Type","application/json")
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        answer = response_body.decode('utf-8')
    else:
        print("Error Code:" + rescode)

    json_answer = json.loads(answer)

    count = 1
    
    if False == os.path.isdir(path + search_key):
        os.mkdir(path + search_key+ '/')       

    save_path = path + search_key + '/'
    
    json_answer = json_answer["items"]

    for i in json_answer:
        try:
            link = i["link"]
            urllib.request.urlretrieve(link, save_path + str(count) +'.jpg')
            count = count + 1
        except (HTTPError, URLError) as e:
            count = count - 1
            print(link, 'ERROR :', e)
            pass


search_keys = ["아이유", "이달의소녀 츄"]
# 다중 검색 가능 Ex) ['검색어1' , '검색어2', ....]
search_count = 100 
# 검색할 이미지 수 최대 100

start = time.time()
client_id = "네이버 Key_ID"
client_secret = "네이버 Key_secret"
path = "D:/code/Naver_C/pi/"

if type(search_keys) == list:
    for search_key in search_keys:
        naver_api(search_key, search_count, client_id, client_secret, path)

else:        
    naver_api(search_keys, search_count, client_id, client_secret, path)

print(time.time() - start)


