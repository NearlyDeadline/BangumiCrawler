'''
Date: 2020-11-10 19:58:06
LastEditors: Mike
LastEditTime: 2020-11-12 17:57:50
FilePath: \BangumiCrawler\request_json.py
'''

import requests
import encodings
import random
import unicodedata
from bs4 import BeautifulSoup
import lxml

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
    text = requests.get(url, headers=headers).text.replace("\\/", "/").replace('\\r\\n', '').encode().decode("unicode_escape")
    text = unicodedata.normalize('NFKD', text)
    return text

'''
description: 输入page页号，获取该页24个作品id，用于get_subject_json进一步获取详细信息
param {int} page
return {[int]} 该页全部id，24个 
'''
def get_subject_id(page):
    subjectIDList = []
    headers = {
        'User-Agent': random.choice(userAgents)
        }
    url = 'https://bgm.tv/anime/browser/?sort=rank&page=' + str(page)
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, 'lxml')
    result = soup.findAll('a', class_="l")
    strList = []
    for i in result:
        strList.append(i["href"])
    strList = strList[3:27]
    for s in strList:
        s = s[9:]
        subjectIDList.append(s)
    
    return subjectIDList

if __name__ == "__main__":
    import json
    d = json.loads((get_subject_json(326)))