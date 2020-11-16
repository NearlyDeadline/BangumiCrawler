'''
Date: 2020-11-10 20:23:40
LastEditors: Mike
LastEditTime: 2020-11-16 23:07:34
FilePath: \BangumiCrawler\writer.py
'''

from request_json import get_subject_json, get_subject_id
from multiprocessing import Process
import json
from define import Bangumi

class WriterProcess (Process):
    __beginPage = 0 # int, 开始爬取的页码，包括自己
    __endPage = 0 # int, 结束爬取的页码，不包括自己
    __bangumiQueue = None # 存入Bangumi对象的队列

    def __init__(self, beginPage, endPage, bangumiQueue):           
        '''
        description: 写者进程。根据网页页码范围先从网页获取ID，再从API网站获取具体信息JSON，将其简化后放入队列供读者调用

        param {int} beginPage，开始爬取的页码，包括该页
        
        param {int} endPage，结束爬取的页码，不包括该页

        param {multiprocessing.Queue} bangumiQueue，存放爬取结果的队列
        '''
        Process.__init__(self)
        self.__beginPage = beginPage
        self.__endPage = endPage
        self.__bangumiQueue = bangumiQueue

    def run(self):          
        '''
        description: 写者爬虫进程主函数
        '''
        for page in range(self.__beginPage, self.__endPage):
            bangumiIDList = get_subject_id(page)
            for bangumiID in bangumiIDList:
                try:
                    subjectJsonDict = json.loads(get_subject_json(bangumiID), strict=False)
                    if isinstance(subjectJsonDict, dict) and subjectJsonDict.get("code", None) == None and Bangumi.shouldInclude(subjectJsonDict):
                    # 如果读取到了一个字典，并且没有code一栏，视为有效数据
                    # 我也不知道为什么bgm.tv设置成只有错误才返回错误码
                    # strict=False: ID=62285, 16805时出现奇怪的字符
                        try:
                            self.__bangumiQueue.put(Bangumi(subjectJsonDict))
                        except Exception as e:
                            log = open("JsonErrorLog.txt", "a", encoding="utf-8")
                            log.write("ID为" + str(bangumiID) + "的作品出现异常：" + str(e) + "\n")
                            log.close()
                except Exception as e:
                    log = open("JsonErrorLog.txt", "a", encoding="utf-8")
                    log.write("ID为" + str(bangumiID) + "的作品出现异常：" + str(e) + "\n")
                    log.close()
