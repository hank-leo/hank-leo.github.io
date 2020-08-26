---
title: "Scrapy框架:Scrapy+MongoDB实战:抓取并保存IT之家博客新闻"
date: 2019-12-06
draft: false
tags: ["Scrapy"]
categories: ["Scrapy框架学习"]
---
#### 创建项目
```
scrapy startproject ithome

cd ithome
scrapy genspider -t crawl news ithome.com
```

#### 编写items.py文件
```
# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class IthomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #文章标题
    title = scrapy.Field()
    #文章url
    url = scrapy.Field()
    #来源
    source = scrapy.Field()
    #来源url
    source_url = scrapy.Field()
    #发布日期
    release_大特＝ scrapy.Field()
    #作者
    author = scrapy.Field()
    #关键词
    key_words = scrapy.Field()
```

#### 编写爬虫文件 news.py
```
# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ithome.items import IthomeItem
import datatime

class NewsSpider(CrawlSpider):
    name = 'news'
    allowed_domains = ['ithome.com']
    start_urls = ['http://www.ithome.com/0/411/151.htm']

    rules = (
        #文章URL形如http://www.ithome.com/0/411/369.htm
        # 根据后三段数字来提取所有的文章url并跟进处理数据
        Rule(LinkExtractor(allow=r'/\d/\d{3}/\d{3}'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = IthomeItem()
        #文章url
        item['url'] = response.url
        #文章标题
        item['title'] = response.css('.post_title > h1::text').extract_first()
        #文章作者
        item['author'] = response.css('#author_baidu strong::text').extract_first()
        #文章来源
        item['source'] = response.css('#source_baidu > a::text').extract_first()
        #文章来源url
        item['source_url'] = response.css('#source_baidu > a::attr(href)').extract_first()
        #关键词
        item['key_words'] = response.css('.hot_tags > span a::text').extract()
        return item
    
    def close(spider, reason):
        self.crawler.stats.set_value('finish_time', datetime.datetime.now())
```

#### 编写管道pipelines.py
```
# -*- coding: utf-8 -*-
# Define your item pipelines here
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from scrapy.exceptions import DropItem
import datetime

class IthomePipeline(object):
    #定义集合ithome_news
    collection = 'ithome_news'

    def __init__(self, mongo_uri, mongo_db, stats):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.stats = stats

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            #从settings.py中获取MONGODB数据库连接信息，数据统计参数
            mongo_uri = crawler.settings.get('MONGO_URI')
            mongo_db = crawler.settings.get('MONGO_DB')
            stats = crawler.stats,
        )
    
    #爬虫启动时打开数据库
    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        #开启爬虫时将结束时间写入数据集参数start中
        self.stats.set_value(''start), datetime.datetime.now())
    
    #爬虫关闭时关闭数据库连接
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        #如果抓取的item中含有title,则为有效数据，保存，否则丢弃
        if not item['title']:
            raise DropItem("数据不完整，丢弃: {}".format(item))
        else:
            self.db[self.collection].insert_one(dict(item))
        return item
```

#### 编写settings.py
```
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'ithome.pipelines.IthomePipeline': 300,
}


#当爬取到10000条数据时关闭爬虫
CLOSESPIDER_ITEMCOUNT = 10000

#MongoDB
MONGO_URI = 'localhost:27017'
MONGO_DB = 'ithome'
```