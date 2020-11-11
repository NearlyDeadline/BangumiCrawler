'''
Date: 2020-11-10 21:04:33
LastEditors: Mike
LastEditTime: 2020-11-11 18:43:15
FilePath: \BangumiCrawler\bangumi_queue.py
'''

from multiprocessing import Lock

class RunningWriterProcessCounter:
    # int: 
    __processCount = 0

    __lock = Lock()
    
    @classmethod
    def __init__(cls, num):
        cls.__processCount = num

    @classmethod
    def getCount(cls): # cls作为参数是王八的屁股——规定
        return cls.__processCount

    @classmethod
    def run(cls):
        cls.__lock.acquire()
        cls.__processCount -= 1
        cls.__lock.release()

    @classmethod
    def terminate(cls):
        cls.__lock.acquire()
        cls.__processCount += 1
        cls.__lock.release()
        