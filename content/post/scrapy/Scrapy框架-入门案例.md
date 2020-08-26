---
title: 'Scrapy框架:入门案例'
date: 2019-12-04
draft: false
tags: ["Scrapy"]
categories: ["Scrapy框架学习"]
---
#### 创建项目:
```
scrappy start project maitian
```

#### 明确要抓取的字段items.py
```
import scrapy

class MaitianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    district = scrapy.Field()
```

#### 在spider目录下创建爬虫文件: zufang_spider.py
2.1 创建一个类，并继承scrapy的一个子类: ```scrapy.Spider```
2.2 自定义爬取名,  ```name=""``` 后面运行框架需要用到；
2.3 定义爬取目标网址
2.4 定义scrapy的方法

下面是简单项目:
```
import scrapy
from maitian.items import MaitianItem

class MaitianSpider(scrapy.Spider):
    name = "zufang"
    start_urls = ['http://bj.maitian.cn/zfall/PG1']

    def parse(self, response):
        for zufang_itme in response.xpath('//div[@class="list_title"]'):
            yield {
                'title': zufang_itme.xpath('./h1/a/text()').extract_first().strip(),
                'price': zufang_itme.xpath('./div[@class="the_price"]/ol/strong/span/text()').extract_first().strip(),
                'area': zufang_itme.xpath('./p/span/text()').extract_first().replace('㎡', '').strip(),
                'district': zufang_itme.xpath('./p//text()').re(r'昌平|朝阳|东城|大兴|丰台|海淀|石景山|顺义|通州|西城')[0],
            }

        next_page_url = response.xpath(
            '//div[@id="paging"]/a[@class="down_page"]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
```

#### 在settings.py文件中设置数据保存到数据库
```
.
.
.

ITEM_PIPELINES = {'maitian.pipelines.MaitianPipeline': 300,}

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = 'maitian'
MONGODB_DOCNAME = 'zufang'
```

#### 通过管道pipelines.py连接上面的操作
```
import pymongo
from scrapy.conf import settings

class MaitianPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DBNAME']
        client = pymongo.MongoClient(host=host, port=port)
        db = client[db_name]
        self.post = db[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        zufang = dict(item)
        self.post.insert(zufang)
        return item
```

其中 middlewares.py 文件暂不处理

以上简单的scrapy爬虫项目搭建完毕了