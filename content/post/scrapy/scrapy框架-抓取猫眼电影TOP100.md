---
title: 'Scrapy框架:抓取猫眼电影TOP100'
date: 2019-12-04
draft: false
tags: ["Scrapy"]
categories: ["Scrapy框架学习"]
---

需求：
抓取的数据为电影名称、主演、上映日期、评分。将抓取的数据保存到maoyantop100.json文件，并将文件作为附件通过邮件发送给接收人。

#### 创建项目
```
scrapy startproject maoyan

scrapy genspider -t crawl top100 maoyan.com
```

#### 编写items.py
```
# -*- coding: utf-8 -*-

import scrapy

class MaoyanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 电影名称
    name = scrapy.Field()
    # 主演
    actors = scrapy.Field()
    # 上映时间
    releasetime = scrapy.Field()
    # 评分
    score = scrapy.Field()
```

#### 编写管道pipelines.py
```
# -*- coding: utf-8 -*-

import json

class MaoyanPipeline(object):
    # 爬虫启动时创建文件maoyan.json
    def open_spider(self,spider):
        self.file = open('maoyantop100.json', 'w')

    # 爬虫关闭时关闭文件
    def close_spider(self,spider):
        self.file.close()

    # 将抓取数据写入json文件
    def process_item(self, item, spider):
        line = json.dumps(dict(item),ensure_ascii=False) + "\n"
        self.file.write(line)
        return item
```

#### 编写爬虫文件top100.py
```
# -*- coding: utf-8 -*-
import scrapy
from scrapy.mail import MailSender
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from maoyan.items import MaoyanItem

class Top100Spider(CrawlSpider):
    name = 'top100'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board/4']

    # 跟进每页电影目录
    rules = (
        Rule(LinkExtractor(allow=r'offset'),callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        movies = response.css('dd')
        for movie in movies:
            item = MaoyanItem()
            item['name'] = movie.css('a::attr(title)').extract_first()
            item['actors'] = movie.css('.star::text').re_first(r'主演：(.*)')
            item['releasetime'] = movie.css('.releasetime').re_first(r'上映时间：(.*)</p>')
            # 使用正则获取评分的组成部分,如[9,.,7]，分别为评分的整数，'.'，小数部分，组合之后9.7添加到item中
            score = movie.css('.score').re(r'\d|\.')
            item['score'] = ''.join(score)
            yield item

    def closed(self,reason):
        # 使用settings中的设置初始化邮件实例
        mail = MailSender.from_settings(self.settings)
        # 将需要发送的附件数据使用‘rb’模式打开
        files = open('./maoyantop100.json', 'rb')
        # 注意attachment是一个迭代器，每一个数据包含三个部分：
        # 1.附件的文件名
        # 2.附件格式
        # 3.需要发送的附件
        attachment = [('maoyan_top_100_movies.json','application/json', files)]
        # 发送邮件，to指定接收人列表，subject邮件主题，body邮件正文，attachs附件，mimetype邮件正文类型
        mail.send(
            to=['xxx@163.com'],
            subject=u'maoyan movie',
            body=u'this is a test',
            attachs=attachment,
            mimetype='text/plain',
            )
        # 关闭文件
        files.close()
```

#### 编写settings.py
```
# -*- coding: utf-8 -*-

BOT_NAME = 'maoyan'

SPIDER_MODULES = ['maoyan.spiders']
NEWSPIDER_MODULE = 'maoyan.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
  'Accept-Language': 'zh-CN,zh;q=0.9',
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'maoyan.pipelines.MaoyanPipeline': 300,
}

# 发送邮件设置
# 指定邮件发送方
MAIL_FROM = 'xxx@163.com'
# 邮件发送服务器
MAIL_HOST = 'smtp.163.com'
# 发送人
MAIL_USER = 'xxx'
# 注意，这是授权码，不是邮箱密码，不同邮件获取授权码方式不一样。
MAIL_PASS = '******'
```
