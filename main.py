'''
Date: 2020-11-10 09:54:57
LastEditors: Mike
LastEditTime: 2020-11-11 23:39:49
FilePath: \BangumiCrawler\main.py
'''
from py2neo import Graph, Node, Relationship
from py2neo.matching import *

if __name__ == "__main__":
    graph = Graph(password="123456")
    graph.delete_all()

    node1 = Node("人物")
    node1["bid"] = 1234
    node1["name"] = "孙博文"

    node2 = Node("University", name="TestSchool")
    graph.create(node1)
    graph.create(node2)

    

    nodes = NodeMatcher(graph)
    node4 = nodes.match("人物", name="孙博文").first()
    if node4:
        teststr2 = '测试关系'
        relationship1 = Relationship(node4, "%s" % teststr2 , node2)
        graph.create(relationship1)
    
    relationship2 = Relationship(node4, "%s" % teststr2 , node2)
    graph.create(relationship2)
    # else:
    #     node4 = Node("City", name="TestCity")
    #     graph.create(node4)
    # node4 = nodes.match("Person", name="Mike").first()
    # node5 = nodes.match("University", name="TestSchool").first()

    # relations = RelationshipMatcher(graph)
    # rs3 = relations.match((node4, node5), "Study at", since=2017).first()
    # if rs3:
    #     print(rs3)
    # else:
    #     print("Not Found")

# from writer import WriterProcess
# from multiprocessing import Queue
# from bangumi_queue import RunningWriterProcessCounter

# if __name__ == "__main__":
#     writeCount = 4 # 写者爬虫进程数量
#     processRange = 2 # 每个进程负责爬多少个ID
#     processShift = 1 # 每个进程的固定偏移

#     bangumiQueue = Queue()
#     processList = []
#     for i in range (0, writeCount):
#         process = WriterProcess(i * processRange + processShift, (i+1) * processRange + processShift, bangumiQueue)
#         processList.append(process)
#         process.start()
#     for p in processList:
#         p.join()
    