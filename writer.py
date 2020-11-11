'''
Date: 2020-11-10 20:23:40
LastEditors: Mike
LastEditTime: 2020-11-11 20:41:16
FilePath: \BangumiCrawler\writer.py
'''

from request_json import get_subject_json
from multiprocessing import Process
import json
from define import Bangumi

class WriterProcess (Process):
    __beginID = 0 # int, 开始爬取的id，包括自己
    __endID = 0 # int, 结束爬取的id，不包括自己
    __bangumiQueue = None # 存入Bangumi对象的队列

    def __init__(self, beginID, endID, bangumiQueue):
        Process.__init__(self)
        self.__beginID = beginID
        self.__endID = endID
        self.__bangumiQueue = bangumiQueue

    '''
    description: 写者爬虫进程主函数。根据ID范围从API网站获取JSON，将其简化后放入队列供读者调用
    param {*} self
    return {*}
    '''
    def run(self):
        for bangumiID in range(self.__beginID, self.__endID):
            subjectJsonDict = json.loads(get_subject_json(bangumiID))
            if isinstance(subjectJsonDict, dict) and subjectJsonDict.get("code", None) == None and Bangumi.shouldInclude(subjectJsonDict):
                # 如果读取到了一个字典，并且没有code一栏，视为有效数据
                # 我也不知道为什么bgm.tv设置成只有错误才返回错误码
                self.__bangumiQueue.put(Bangumi(subjectJsonDict))
            else: # 结果不是字典，或者有code一栏，视为无效数据
                pass
