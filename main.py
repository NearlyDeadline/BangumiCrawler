'''
Date: 2020-11-10 09:54:57
LastEditors: Mike
LastEditTime: 2020-11-11 18:42:54
FilePath: \BangumiCrawler\main.py
'''
# from py2neo import Graph, Node, Relationship
# from py2neo.matching import *

# if __name__ == "__main__":
#     graph = Graph(password="123456")
#     graph.delete_all()

#     node1 = Node("Person", name="Mike")
#     node2 = Node("University", name="TestSchool")
#     graph.create(node1)
#     graph.create(node2)

#     relationship1 = Relationship(node1, "Study at", node2)
#     relationship1["since"] = 2017
#     graph.create(relationship1)

#     nodes = NodeMatcher(graph)
#     node4 = nodes.match("City", name="TestCity").first()
#     if node4:
#         print("已找到，不再创建")
#     else:
#         node4 = Node("City", name="TestCity")
#         graph.create(node4)
#     node4 = nodes.match("Person", name="Mike").first()
#     node5 = nodes.match("University", name="TestSchool").first()

#     relations = RelationshipMatcher(graph)
#     rs3 = relations.match((node4, node5), "Study at", since=2017).first()
#     if rs3:
#         print(rs3)
#     else:
#         print("Not Found")

from writer import WriterProcess
from multiprocessing import Queue

if __name__ == "__main__":
    writerCount = 4
    bangumiQueue = Queue()
    for i in range (0, writerCount):
        process = WriterProcess(i+1, 2*(i+1), bangumiQueue)
        process.start()

    