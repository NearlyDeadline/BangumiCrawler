<!--
 * @Date: 2020-11-19 14:35:30
 * @LastEditors: Mike
 * @LastEditTime: 2020-11-19 15:18:16
 * @FilePath: \BangumiCrawler\readme.md
-->
# Bangumi Crawler

## 安装与运行
### 必需：

- Python
- Neo4j

#### 库:

- requests
- lxml
- bs4
- py2neo


## 用途

爬取https://bgm.tv排名前列的动画，将其插入Neo4j数据库中

### 节点定义及其属性

- 作品：名称、评分值、评分人数、排名

- 人物：姓名

- 角色：姓名、性别

- 标注：名称

注：作品节点在程序中有另外一些属性，但考虑到Neo4j数据库无需存放如此多的属性，（Neo4j数据库旨在强调各节点间的关系，而非节点其他信息，存放这些信息可以用SQL系数据库解决）爬取这些属性的代码在程序中被注释掉。
### 关系定义及其属性

- 出演：角色->作品

- 导演：人物->作品

- 脚本：人物->作品

- 配音：人物->角色

- 拥有标注：作品->标注。属性：标注人数

### 程序参数
以下列表各项均指代码文件名，扩展名均为py
- main:
```
writerCount: 爬虫进程数量
pageRange: 每个进程负责爬多少页
pageShift: 页号偏移
```
程序建立```writerCount```个爬虫进程。令```0 <= i < writerCount```，第i个进程爬取第```pageShift + i * pageRange```到```pageShift + (i + 1) * pageRange```页（左闭右开区间）

- reader:
```
class Neo4jConfig:
    host: 数据库主机地址（一般为127.0.0.1环回，无需修改）
    user: 数据库登录名（一般为neo4j，无需修改）
    password: 数据库密码（需要在Neo4j创建数据库时自行设定）
```

## 其他
- records文件夹内存放了作者爬取到的数据

- writer运行时会创建JsonErrorLog.txt，记录爬取中遇到的异常
