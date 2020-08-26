---
title: 'Scrapy框架:统计数据收集'
date: 2019-12-04
draft: false
tags: ["Scrapy"]
categories: ["Scrapy框架学习"]
---

通过stats属性来使用数据收集器
```
class ExtensionThatAccessStats(object):
    
    def __init__(self, stats):
        self.stats = stats
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.stats)
```

设置数据
```
stats.set_value('hostname', socket.gethostname())
```

增加数据值
```
stats.inc_value('pages_crawled')
```

当新的值比原来的值大时设置数据
```
stats.max_value('max_items_scraoed', value)
```

当新的值比原来的值小时设置数据
```
stats.min_value('min_free_memory_percent', value)
```

获取数据
```
stats.get_value('pages_crawled')
```

获取所有数据
```
stats.get_stats()
```

示例：统计名人名言网站(http://quotes.toscrape.com/)标签为love的名言数量

创建项目
```
scrapy startproject tagcount
```

创建爬虫
```
scrapy genspider tags quotes.toscrape.com
```

编写tags.py文件
```
# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from tagcount.items import TagcountItem


class TagsSpider(scrapy.Spider):
    name = 'tags'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = TagcountItem()
            # 提取内容数据
            item['author'] = quote.css('.author::text').extract_first()
            item['content'] = quote.css('.text::text').extract_first()
            item['tag'] = quote.css('.tag::text').extract()
            if 'love' in item['tag']:
                # 如果“love”在获取的tag内容中，则“love”统计数量+1
                self.crawler.stats.inc_value('love')
            yield item

        next_page = response.css('.next > a::attr(href)').extract_first()
        if next_page is not None:
            yield Request(response.urljoin(next_page), callback=self.parse)
```

编写items.py文件
```
# -*- coding: utf-8 -*-
# Define here the models for your scraped items
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TagcountItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 标签
    tag = scrapy.Field()
```

运行爬虫文件，输出结果如下：
```
2019-12-01 14:12:35 [scrapy.core.scraper] DEBUG: Scraped from <200 http://quotes.toscrape.com/page/10/>
{'author': 'George R.R. Martin',
 'content': '“... a mind needs books as a sword needs a whetstone, if it is to '
            'keep its edge.”',
 'tag': ['books', 'mind']}
2019-12-01 14:12:35 [scrapy.core.engine] INFO: Closing spider (finished)
2019-12-01 14:12:35 [scrapy.statscollectors] INFO: Dumping Scrapy stats:
{'downloader/request_bytes': 2870,
 'downloader/request_count': 11,
 'downloader/request_method_count/GET': 11,
 'downloader/response_bytes': 24812,
 'downloader/response_count': 11,
 'downloader/response_status_count/200': 10,
 'downloader/response_status_count/404': 1,
 'finish_reason': 'finished',
 'finish_time': datetime.datetime(2019, 12, 1, 6, 12, 35, 567519),
 'item_scraped_count': 100,
 'log_count/DEBUG': 111,
 'log_count/INFO': 9,
 'love': 14,
 'memusage/max': 48644096,
 'memusage/startup': 48644096,
 'request_depth_max': 9,
 'response_received_count': 11,
 'robotstxt/request_count': 1,
 'robotstxt/response_count': 1,
 'robotstxt/response_status_count/404': 1,
 'scheduler/dequeued': 10,
 'scheduler/dequeued/memory': 10,
 'scheduler/enqueued': 10,
 'scheduler/enqueued/memory': 10,
 'start_time': datetime.datetime(2019, 12, 1, 6, 12, 2, 175884)}
2019-12-01 14:12:35 [scrapy.core.engine] INFO: Spider closed (finished)
```