---
title: "Scrapy框架 基本命令"
date: 2019-12-04
draft: false
tags: ["Scrapy"]
categories: ["Scrapy框架学习"]
---

#### 创建爬虫项目
```
scrapy startproject [项目名称]
```

#### 创建爬虫文件
```
scrapy genspider +文件名+网址
```

#### 运行(crawl)
```
scrapy crawl 爬虫名称

# -o  output 输出数据到文件
scrapy crawl [爬虫名称] -o zufang.json
scrapy crawl [爬虫名称] -o zufang.csv
```

#### check检查错误
```
scrapy check
```

#### list返回项目所有spider
```
scrapy list
```

#### view 存储、打开网页
```
scrapy view http://www.baidu.com
```

#### scrapy shell, 进入终端
```
scrapy shell https://www.baidu.com
```

#### scrapy runspider
```
scrapy runspider zufang_spider.py
```