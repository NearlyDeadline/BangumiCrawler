'''
Date: 2020-11-10 21:04:33
LastEditors: Mike
LastEditTime: 2020-11-11 20:40:56
FilePath: \BangumiCrawler\bangumi_queue.py
'''

from multiprocessing import Lock, Value, Queue

class RunningWriterProcessCounter:
    # int: 写者进程数目
    __processCount = Value('i', 4)
    
    __lock = Lock()

    @staticmethod
    def getCount(): # cls作为参数是王八的屁股——规定
        return RunningWriterProcessCounter.__processCount.value

    @staticmethod
    def run():
        RunningWriterProcessCounter.__lock.acquire()
        RunningWriterProcessCounter.__processCount.value -= 1
        print(RunningWriterProcessCounter.__processCount.value)
        RunningWriterProcessCounter.__lock.release()

    @staticmethod
    def terminate():
        RunningWriterProcessCounter.__lock.acquire()
        RunningWriterProcessCounter.__processCount.value += 1
        RunningWriterProcessCounter.__lock.release()
        
if __name__ == "__main__":
    print(RunningWriterProcessCounter.getCount())
    RunningWriterProcessCounter.run()
    print(RunningWriterProcessCounter.getCount())