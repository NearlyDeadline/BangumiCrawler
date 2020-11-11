'''
Date: 2020-11-10 20:30:04
LastEditors: Mike
LastEditTime: 2020-11-11 15:40:48
FilePath: \BangumiCrawler\reader.py
'''

from py2neo import Graph, Node, Relationship
from py2neo.matching import *
from multiprocessing import Process

class ReaderProcess(Process):

    def run(self):
        pass