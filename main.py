'''
Date: 2020-11-10 09:54:57
LastEditors: Mike
LastEditTime: 2020-11-12 10:07:58
FilePath: \BangumiCrawler\main.py
'''

from writer import WriterProcess
from multiprocessing import Queue
from bangumi_queue import RunningWriterProcessCounter

if __name__ == "__main__":
    writeCount = 4 # 写者爬虫进程数量
    processRange = 2 # 每个进程负责爬多少个ID
    processShift = 1 # 每个进程的固定偏移

    bangumiQueue = Queue()
    processList = []
    for i in range (0, writeCount):
        process = WriterProcess(i * processRange + processShift, (i+1) * processRange + processShift, bangumiQueue)
        processList.append(process)
        process.start()
    for p in processList:
        p.join()
    