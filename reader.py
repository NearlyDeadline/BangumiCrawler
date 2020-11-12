'''
Date: 2020-11-10 20:30:04
LastEditors: Mike
LastEditTime: 2020-11-12 14:03:17
FilePath: \BangumiCrawler\reader.py
'''

from py2neo import Graph, Node, Relationship, Schema
from py2neo.matching import *
from multiprocessing import Process, Queue

class Neo4jConfig:
    host = "127.0.0.1"
    user = "neo4j"
    password = "123456"
    def __init__(self):
        graph = Graph(host=Neo4jConfig.host, user=Neo4jConfig.user, password=Neo4jConfig.password)
        graph.delete_all()
        schema = Schema(graph)

        schema.create_uniqueness_constraint("作品", "bid")
        schema.create_index("作品", "name")

        schema.create_uniqueness_constraint("角色", "cid")
        schema.create_index("角色", "name")

        schema.create_index("人物", "pid")
        schema.create_uniqueness_constraint("人物", "name")


class ReaderProcess:
    __bangumiQueue = None # multiprocessing.Queue，存入Bangumi对象的队列
    __writerProcessList = [] # [multiprocessing.Process]，所有写者进程的列表

    def __init__(self, bangumiQueue, writerProcessList):
        self.__bangumiQueue = bangumiQueue
        self.__writerProcessList = writerProcessList

    def start(self):
        self.run()

    def run(self):
        graph = Graph(host=Neo4jConfig.host, user=Neo4jConfig.user, password=Neo4jConfig.password)

        while True:
            '''
            while self.__bangumiQueue.empty() and filter(lambda p : p.is_alive(), self.__writerProcessList):
                pass
            # 队列已空，但还有工作中的写者进程，读者进程应该等待，直到队列不空退出循环或者写者进程全部结束
            if self.__bangumiQueue.empty() and not filter(lambda p : p.is_alive(), self.__writerProcessList):
                break
            # 队列已空、并且没有正在工作的写者进程时，读者进程应该结束工作
            '''

            bangumi = self.__bangumiQueue.get()
            nodematcher = NodeMatcher(graph)
            bangumiNode = nodematcher.match("作品", bid=str(bangumi.bangumiID)).first()
            if not bangumiNode: # 保证作品不重复
                bangumiNode = Node("作品")
                bangumiNode["bid"] = bangumi.bangumiID
                bangumiNode["name"] = bangumi.name
                bangumiNode["集数"] = bangumi.count
                bangumiNode["放送开始"] = bangumi.pubTime
                bangumiNode["排名"] = bangumi.rank
                bangumiNode["评分人数"] = bangumi.ratingTotal
                bangumiNode["评分值"] = bangumi.ratingScore
                bangumiNode["想看人数"] = bangumi.collection.wish
                bangumiNode["看过人数"] = bangumi.collection.collect
                bangumiNode["在看人数"] = bangumi.collection.doing
                bangumiNode["搁置人数"] = bangumi.collection.onHold
                bangumiNode["抛弃人数"] = bangumi.collection.dropped
                
                graph.create(bangumiNode)
                
                # 遍历该作品的所有角色，去创建角色结点、作品与角色的关系
                for character in bangumi.characters:
                    characterNode = nodematcher.match("角色", cid=str(character.characterID)).first()
                    if not characterNode: # 未找到，创建角色结点
                        characterNode = Node("角色")
                        characterNode["cid"] = character.characterID
                        characterNode["name"] = character.name
                        characterNode["性别"] = str(character.gender)

                        graph.create(characterNode)

                    # 创建作品与角色的关系
                    relationship = Relationship(characterNode, "出演", bangumiNode)
                    graph.create(relationship)

                    # 创建角色与人设的关系，注意人设的人物id为-1，需要用名字查找
                    settingNode = nodematcher.match("人物", name=character.setting.name).first()
                    if not settingNode:
                        settingNode = Node("人物")
                        settingNode["pid"] = character.setting.personID
                        settingNode["name"] = character.setting.name

                        graph.create(settingNode)
                    
                    relationship = Relationship(settingNode, "设定", characterNode)
                    graph.create(relationship)

                    # 遍历该角色的所有配音，去创建人物结点、配音与角色的关系
                    for actor in character.actors:
                        personNode = nodematcher.match("人物", pid=str(actor.personID)).first()
                        if not personNode: # 未找到，创建人物结点
                            personNode = Node("人物")
                            personNode["pid"] = actor.personID
                            personNode["name"] = actor.name

                            graph.create(personNode)

                        # 创建配音与角色的关系        
                        relationship = Relationship(personNode, "配音", characterNode)
                        graph.create(relationship)

                # 遍历该作品的所有制作人员，去创建人物结点、人物与作品的关系
                for staffPerson in bangumi.staff:
                    staffNode = nodematcher.match("人物", pid=str(staffPerson.personID))
                    if not staffNode:
                        staffNode = Node("人物")
                        staffNode["pid"] = staffPerson.personID
                        staffNode["name"] = staffPerson.name

                        graph.create(staffNode)

                    relationship = Relationship(staffNode, "%s" % staffPerson.personJob.name, bangumiNode)
                    graph.create(relationship)

if __name__ == "__main__":
    from writer import WriterProcess
    Neo4jConfig()
    q = Queue()
    wp = WriterProcess(9717,9718,q)
    l = []
    l.append(wp)
    wp.start()
    rp = ReaderProcess(q, l)
    rp.start()
    wp.join()
    print("结束")
