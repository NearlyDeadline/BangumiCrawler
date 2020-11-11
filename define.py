'''
Date: 2020-11-10 20:26:29
LastEditors: Mike
LastEditTime: 2020-11-11 18:45:39
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
    param {int} personID
    param {str} name
    param {PersonJob} personJob
    return {*}
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

    # str: 性别"info"."gender"，不是每个角色都有这一项
    gender = ""

    # [Person]: 配音"crt"."actors"
    actors = []

    # Person: 人设"crt"."info"."人设"，不是每个角色都有这一项
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
    '''
    description: 输入从api爬取到的全部数据，选择有用的信息进行存储，进行预备的反序列化
    param {*} self
    param {*} subjectJsonDict，已经被读取为dict形式的json
    return {*}
    '''
    def __init__(self, subjectJsonDict):
        self.bangumiID = subjectJsonDict["id"]
        self.name = subjectJsonDict["name_cn"]
        self.count = subjectJsonDict["eps_count"]
        self.pubTime = subjectJsonDict["air_date"]
        self.rank = subjectJsonDict["rank"]

        # "rating"
        self.ratingTotal = subjectJsonDict["rating"]["total"]
        self.ratingScore = subjectJsonDict["rating"]["score"]
        
        # "rating"."count": 数组第i位表示评分为i+1的人数
        for i in range(1, 11):
            self.ratingScoreList[i - 1] = subjectJsonDict["rating"]["count"][str(i)]

        # "collection"
        self.collection.wish = subjectJsonDict["collection"]["wish"]
        self.collection.collect = subjectJsonDict["collection"]["collect"]
        self.collection.doing = subjectJsonDict["collection"]["doing"]
        self.collection.onHold = subjectJsonDict["collection"]["on_hold"]
        self.collection.dropped = subjectJsonDict["collection"]["dropped"]

        # "crt"，只收录主角
        for characterDict in filter(lambda characterDict: characterDict["role_name"] == "主角", subjectJsonDict["crt"]):
            crt = Character()  # character简写，代表一个虚拟角色
            crt.characterID = characterDict["id"]
            crt.name = characterDict["name_cn"]
            
            if (characterDict["info"].get("gender", None)):
                crt.gender = characterDict["info"]["gender"]
            else:
                crt.gender = None

            if (characterDict["info"].get("人设", None)):
                crt.setting = Person(-1, characterDict["info"]["人设"], PersonJob.人物设定)
            else:
                crt.setting = None

            crt.actors = []
            for actorDict in characterDict["actors"]:
                crt.actors.append(Person(actorDict["id"], actorDict["name"], PersonJob.配音))

            self.characters.append(crt)
            
        # "staff"，只添加导演和脚本
        for staffDict in subjectJsonDict["staff"]:
            if "导演" in staffDict["jobs"]:
                self.staff.append(Person(staffDict["id"], staffDict["name_cn"],PersonJob.导演))
            if "脚本" in staffDict["jobs"]:
                self.staff.append(Person(staffDict["id"], staffDict["name_cn"],PersonJob.脚本))

    
    '''
    description: 根据评分人数和评分值综合判断该番剧是否值得收录
    param {*} self
    param {dict} subjectJson
    return {Bool} result
    '''
    @staticmethod
    def shouldInclude(subjectJsonDict):
        if subjectJsonDict["type"] != 2: # 不是动画
            return False
        ratingCount = subjectJsonDict["rating"]["total"]
        ratingScore = subjectJsonDict["rating"]["score"]
        if ratingCount < 700 or ratingScore < 6.5:
            # 评分人数少于700人或者评分值低于6.5视为不值得输入的数据
            return False
        return True

    
    # int: "id"
    bangumiID = 0

    # str: 中文名字，"name_cn"
    name = ""

    # int: 集数，"eps_count"
    count = 0

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
    collection = Collection()

    # [Character]: 主角
    characters = []

    # [Person]: 主要制作人员
    staff = []

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
