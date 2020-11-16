'''
Date: 2020-11-10 20:26:29
LastEditors: Mike
LastEditTime: 2020-11-16 23:04:55
FilePath: \BangumiCrawler\define.py
'''  

from enum import Enum
class PersonJob(Enum):
    配音 = 1
    人物设定 = 2
    导演 = 3
    脚本 = 4

class Person: # 三次元人物，包括：导演/脚本/配音/人设等
    '''
    description: 初始化

    param {int} personID: 人设为-1，其余可在Json中查到

    param {str} name: 一般为"name_cn"，该项为空时用"name"替代
    
    param {PersonJob} personJob: 见PersonJob枚举
    '''
    def __init__(self, personID, name, personJob):
        self.personID = personID
        self.name = name
        self.personJob = personJob

    # int: id
    personID = 0

    # str: 名称，一般是"name_cn"
    name = ""

    # Job: 职责
    personJob = None
    
    
class Character: # 二次元虚拟角色
    # int: "id"
    characterID = 0

    # str: 中文名"name_cn"
    name = ""

    # str: 性别"info"."gender"，不是每个角色都有这一项，没有时值为"未知"
    gender = ""

    # [Person]: 配音"crt"."actors"
    actors = []

    # Person: 人设"crt"."info"."人设"，不是每个角色都有这一项，没有时值为None
    setting = None

    
class Collection:
    # int: "collection"."wish"
    wish = 0

    # int: "collection"."collect"
    collect = 0

    # int: "collection"."doing"
    doing = 0

    # int: "collection"."on_hold"
    onHold = 0

    # int: "collection"."dropped"
    dropped = 0  


class Bangumi:
    # int: "id"
    bangumiID = 0

    # str: 中文名字，"name_cn"
    name = ""

    # str: 播出日期，"air_date"
    pubTime = ""

    # int: 排名，"rank"
    rank = 0

    # int: 评分人数，"rating"."total"
    ratingTotal = 0

    # double: 评分值，"rating"."score"
    ratingScore = 0.0

    # [int]: 各评分值的人数，长度应始终为10。第i位对应给i+1分的人数
    # 是"rating"."count"的反序
    ratingScoreList = [0] * 10

    # 状态
    collection = None

    # [Character]: 主角
    characters = []

    # [Person]: 主要制作人员
    staff = []

    def __init__(self, subjectJsonDict):
        '''
        description: 输入从api爬取到的全部数据，选择有用的信息进行存储，进行初步的反序列化
        
        param {dict} subjectJsonDict，已经被读取为dict形式的json
        '''
        self.bangumiID = subjectJsonDict["id"]
        
        if subjectJsonDict["name_cn"]:
            self.name = subjectJsonDict["name_cn"]
        else:
            self.name = subjectJsonDict["name"]

        self.pubTime = subjectJsonDict["air_date"]
        self.rank = subjectJsonDict["rank"]

        # "rating"
        self.ratingTotal = subjectJsonDict["rating"]["total"]
        self.ratingScore = subjectJsonDict["rating"]["score"]
        
        # "rating"."count": 数组第i位表示评分为i+1的人数
        for i in range(1, 11):
            self.ratingScoreList[i - 1] = subjectJsonDict["rating"]["count"][str(i)]

        # "collection"
        self.collection = Collection()
        self.collection.wish = subjectJsonDict["collection"]["wish"]
        self.collection.collect = subjectJsonDict["collection"]["collect"]
        # ID=35814，粗心网站程序员忘了加doing这一项，需要手动爬一下这个，自己设一下doing的值
        self.collection.doing = subjectJsonDict["collection"]["doing"]
        self.collection.onHold = subjectJsonDict["collection"]["on_hold"]
        self.collection.dropped = subjectJsonDict["collection"]["dropped"]

        # "crt"，只收录主角
        self.characters = []
        if subjectJsonDict["crt"]:
            for characterDict in filter(lambda characterDict: characterDict["role_name"] == "主角", subjectJsonDict["crt"]):
                crt = Character()  # character简写，代表一个虚拟角色
                crt.characterID = characterDict["id"]
                if characterDict["name_cn"]:
                    crt.name = characterDict["name_cn"]
                else:
                    crt.name = characterDict["name"]
                
                if (characterDict["info"]):
                    if (characterDict["info"].get("gender", None)):
                        crt.gender = characterDict["info"]["gender"]
                    else:
                        crt.gender = "未知"

                    if (characterDict["info"].get("人设", None)):
                        crt.setting = Person(-1, characterDict["info"]["人设"], PersonJob.人物设定)
                    else:
                        crt.setting = None

                crt.actors = []
                if characterDict["actors"]:
                    for actorDict in characterDict["actors"]:
                        crt.actors.append(Person(actorDict["id"], actorDict["name"], PersonJob.配音))
        
                self.characters.append(crt) 
        # "staff"，只添加导演和脚本
        self.staff = []
        for staffDict in subjectJsonDict["staff"]:
            if staffDict["name_cn"]:
                staffName = staffDict["name_cn"]
            else:
                staffName = staffDict["name"]
            if "导演" in staffDict["jobs"]:
                self.staff.append(Person(staffDict["id"], staffName,PersonJob.导演))
            if "脚本" in staffDict["jobs"]:
                self.staff.append(Person(staffDict["id"], staffName,PersonJob.脚本))

    
    @staticmethod
    def shouldInclude(subjectJsonDict):        
        '''
        description: 判断该番剧是否值得收录

        param {dict} subjectJson
        
        return {Bool} result
        '''
        if subjectJsonDict["type"] != 2: 
            # 不是动画的不要
            return False
        if "OVA" in subjectJsonDict["name"] or "OAD" in subjectJsonDict["name"]:
            # OVA或者OAD的不要
            return False
        if subjectJsonDict["rating"]["total"] < 1000:
            # 评分人数少于这些人的不要
            return False
        return True

if __name__ == "__main__":
    import json
    test = json.load(open("SubjectMediumExample.json", encoding="utf-8"))
    bangumi = Bangumi(test)
    for crt in bangumi.characters:
        print (crt.name)
        for act in crt.actors:
            print(act.name)
        print ("\n")
    for crt in bangumi.staff:
        print(crt.name)
        print(crt.personJob.name)
