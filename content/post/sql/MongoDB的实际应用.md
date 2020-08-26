---
title: "MongoDB的实际应用"
date: 2019-12-05
draft: false
tags: ["MongoDB"]
categories: ["数据库学习"]
---

### MongoDB基本操作

**1.数据库操作**

使用use DATABASE_NAME创建数据库

```
use maitian
```

如果数据库不存在，就创建数据库，否则切换到指定的数据库

使用show dbs查看所有数据库

```
show dbs
```

使用db.dropDatabase()删除数据库

```
use maitian

db.dropDatabase()
```

**2.集合操作**

在maitian数据库中创建名为zufang的集合

```
use maitian

db.createCollection("zufang")
```

查看所有集合

```
show collections

show tables
```

**3.文档操作**

(1)使用db.collection_name.insert(document)在集合中插入文档

```
db.zufang.insert({"title":"xxxx","price":"8888","area":"233","district":"xxx"})
```

(2)使用db.collection_name.find()查询文档

```
db.zufang.find()
```

可以使用.pretty()方法来使输出数据更易读

```
db.zufang.fin().pretty()
```

**4.Mac上操作MongoDB**

MongoDB启动和关闭

* 启动

```linux
mongod --dbpath /usr/local/mongodb/data
```

* 关闭

```linux
use admin, db.shutdownServer() 
```

