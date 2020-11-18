'''
Date: 2020-11-10 09:54:57
LastEditors: Mike
LastEditTime: 2020-11-18 16:17:27
FilePath: \BangumiCrawler\main.py
'''

from writer import WriterProcess
from multiprocessing import Queue
from reader import ReaderProcess, Neo4jConfig
import sys
sys.setrecursionlimit(1000000) # 为什么需要增加递归深度呢

if __name__ == "__main__":
    writerCount = 4 # 写者爬虫进程数量
    pageRange = 25 # 每个进程负责爬多少页
    pageShift = 1 # 每个进程的固定偏移

    Neo4jConfig()
    
    bangumiQueue = Queue()

    processList = []
    for i in range (0, writerCount):
        process = WriterProcess(i * pageRange + pageShift, (i+1) * pageRange + pageShift, bangumiQueue)
        processList.append(process)
        process.start()
    
    process = ReaderProcess(bangumiQueue)
    process.start()

    for p in processList:
        p.join()
    process.join()
    print("程序结束")
    