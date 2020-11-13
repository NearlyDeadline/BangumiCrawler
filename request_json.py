'''
Date: 2020-11-10 19:58:06
LastEditors: Mike
LastEditTime: 2020-11-13 15:32:15
FilePath: \BangumiCrawler\request_json.py
'''

import requests
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
return {string} text
通过id向api网站发送get请求，对返回的json进行如下处理（以下均为JSON的字面值）：
①将\/替换为/，处理url自带的转义符
②将\r\n去除，处理summary里的一些换行回车符
③将\\替换为//，id=265时有个key值为\\，不知道有什么含义，替换掉
④将\"替换为\\"，处理summary里的\"转义双引号，由于unicode转中文会将\"转变为"，导致json读取失败，因此需要将转中文后的结果替换为\"
⑤按unicode_escape格式解码
⑥调用normalize进行规范化，删除\u3000这种中文空格符
注意：还会残留一些奇奇怪怪的字符，json.loads方法中请将strict置为False
'''
def get_subject_json(id):
    headers = {
        'User-Agent': random.choice(userAgents)
        }
    url = 'https://api.bgm.tv/subject/' + str(id) + '?responseGroup=medium'
    text = requests.get(url, headers=headers).text
    text = text.replace("\\/", "/").replace('\\r\\n', '').replace('\\\\', '//').replace('\\"', '\\\\"')
    # 以下冒号左侧均为字面值
    # \/ : 部分url自带的转义/字符，将前面的反斜杠去掉即可
    # \\ : id=265时，有一个\\为key的键值对。实在不知道有什么含义，干脆替换为//
    # \r\n : 部分summary中出现的换行回车符，去掉
    # \" : 部分summary中出现的转义双引号，被decode后反斜杠消去，使得结果无法转化为json，需要变成\\"，使得字面值变为\"
    text = text.encode().decode("unicode_escape")
    text = unicodedata.normalize('NFKD', text)
    # normalize() : 处理\u3000这种莫名其妙的字符 
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
    result = soup.findAll('a', class_="l") # 为什么bgm.tv会将class名单走一个l？(字母k的后继字母)
    strList = []
    for i in result:
        strList.append(i["href"])
    strList = strList[3:27] # 只有第3-27个是需要的链接，具体参看html示例
    for s in strList:
        s = s[9:] # 前面几位固定为/subject/，正好9个字符，因此从9开始取
        subjectIDList.append(s)
    
    return subjectIDList

if __name__ == "__main__":
    import json
    f = open("ErrorExample.json", "w", encoding="utf-8")
    a = get_subject_json(42707)
    f.write(a)
    f.close()
    print(json.loads(a,strict=False))
