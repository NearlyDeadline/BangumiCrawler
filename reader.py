'''
Date: 2020-11-10 20:30:04
LastEditors: Mike
LastEditTime: 2020-11-11 23:34:07
FilePath: \BangumiCrawler\reader.py
'''

from py2neo import Graph, Node, Relationship
from py2neo.matching import *
from multiprocessing import Process, Queue


class ReaderProcess(Process):
    __bangumiQueue = Queue()

    def __init__(self, bangumiQueue):
        self.__bangumiQueue = bangumiQueue
        
    def run(self):
        graph = Graph(password="123456")

        while True:
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
                bangumiNode["想看人数"] = bangumi.wish
                bangumiNode["看过人数"] = bangumi.collect
                bangumiNode["在看人数"] = bangumi.doing
                bangumiNode["搁置人数"] = bangumi.onHold
                bangumiNode["抛弃人数"] = bangumi.dropped
                
                graph.create(bangumiNode)
                
            # 遍历该作品的所有角色，去创建角色结点、作品与角色的关系
            for character in bangumi.characters:
                characterNode = nodematcher.match("角色", cid=str(character.characterID)).first()
                if not characterNode: # 未找到，创建角色结点
                    characterNode = Node("角色")
                    characterNode["cid"] = character.characterID
                    characterNode["name"] = character.name
                    character["性别"] = character.gender

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

                