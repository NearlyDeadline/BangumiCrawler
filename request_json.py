'''
Date: 2020-11-10 19:58:06
LastEditors: Mike
LastEditTime: 2020-11-10 21:41:48
FilePath: \Bangumi\request_json.py
'''

import requests
import encodings
import random

userAgents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36 Edg/86.0.622.63",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763",
]  # 浏览器UserAgent列表

'''
description: 根据番剧id，访问api网站获取番剧详细信息，将其编码为可直接显示的json
param {int} id: 番剧id
return {string} 包含如下处理：①将"\/"替换为"/" ②从unicode解码
'''
def get_subject_json(id):
    headers = {
        'User-Agent': random.choice(userAgents)
        }
    url = 'https://api.bgm.tv/subject/' + str(id) + '?responseGroup=medium'
    return requests.get(url, headers=headers).text.replace("\/", "/").encode().decode("unicode_escape")
