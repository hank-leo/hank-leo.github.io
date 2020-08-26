---
title: "Scrapy框架:通用爬虫"
date: 2019-12-06
draft: false
tags: ["Scrapy"]
categories: ["Scrapy框架学习"]
---
#### 通用爬虫之CrawlSpider
步骤01: 创建爬虫项目
```
scrapy startproject quotes
```

步骤02: 创建爬虫模版
```
scrapy genspider -t quotes quotes.toscrape.com
```

步骤03: 配置爬虫文件quotes.py
```
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Quotes(CrawlSpider):
	# 爬虫名称
    name = "get_quotes"
    allow_domain = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

# 设定规则
    rules = (
        # 对于quotes内容页URL，调用parse_quotes处理，
      		# 并以此规则跟进获取的链接
        Rule(LinkExtractor(allow=r'/page/\d+'), callback='parse_quotes', follow=True),
      		# 对于author内容页URL，调用parse_author处理，提取数据
        Rule(LinkExtractor(allow=r'/author/\w+'), callback='parse_author')
    )

# 提取内容页数据方法
    def parse_quotes(self, response):
        for quote in response.css(".quote"):
            yield {'content': quote.css('.text::text').extract_first(),
                   'author': quote.css('.author::text').extract_first(),
                   'tags': quote.css('.tag::text').extract()
                   }
	# 获取作者数据方法

    def parse_author(self, response):
        name = response.css('.author-title::text').extract_first()
        author_born_date = response.css('.author-born-date::text').extract_first()
        author_bron_location = response.css('.author-born-location::text').extract_first()
        author_description = response.css('.author-description::text').extract_first()

        return ({'name': name,
                 'author_bron_date': author_born_date,
                 'author_bron_location': author_bron_location,
                 'author_description': author_description
                 })
```

步骤04: 运行爬虫
```
scrapy crawl quotes
```

#### 通用爬虫之CSVFeedSpider
步骤01: 创建项目
```
scrapy startproject csvfeedspider
```

步骤02: 使用csvfeed模版
```
scrapy genspider -t csvfeed csvdata gzdata.gov.cn
```

步骤03: 编写items.py
```
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CsvspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # 姓名
    name = scrapy.Field()
    # 研究领域
    SearchField = scrapy.Field()
    # 服务分类
    Service = scrapy.Field()
    # 专业特长
    Specialty = scrapy.Field()
```

步骤04: 编写爬虫文件csvdata.py
```
# -*- coding: utf-8 -*-
from scrapy.spiders import CSVFeedSpider
from csvfeedspider.items import CsvspiderItem


class CsvparseSpider(CSVFeedSpider):
    name = 'csvdata'
    allowed_domains = ['gzdata.gov.cn']
    start_urls = ['http://gzopen.oss-cn-guizhou-a.aliyuncs.com/科技特派员.csv']
    headers = ['name', 'SearchField', 'Service', 'Specialty']
    delimiter = ','
    quotechar = "\n"

    # Do any adaptations you need here
    def adapt_response(self, response):
       return response.body.decode('gb18030')

    def parse_row(self, response, row):

        i = CsvspiderItem()
        try:
            i['name'] = row['name']
            i['SearchField'] = row['SearchField']
            i['Service'] = row['Service']
            i['Specialty'] = row['Specialty']

        except:
            pass
        yield i
```

步骤05: 运行爬虫文件
```
scrapy crawl csvdata
```

#### 通用爬虫之SitemapSpider
步骤01: 创建项目
```
scrapy startproject cnblogs
```

步骤02: 编写items.py
```
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CnblogsItem(scrapy.Item):
    # define the fields for your item here like:
    # 文章标题
    title = scrapy.Field()
    # 文章url
    url = scrapy.Field()
    # 文章作者
    author = scrapy.Field()
```

步骤03: 在spiders文件夹内创建articles.py
```
from scrapy.spiders import SitemapSpider
from cnblogs.items import CnblogsItem

class MySpider(SitemapSpider):
    name = 'articles'
    # Sitemap 地址
    sitemap_urls = ['http://www.cnblogs.com/sitemap.xml']
    # 从Sitemap中提取url的规则，并指定回调方法
    sitemap_rules = [
        # 抓取 ***/cate/python/**的url，调用parse_python处理
        ('/cate/python/','parse_python')
    ]

    # 回调方法
    def parse_python(self,response):
        articles = response.css('.post_item')

        for article in articles:
            item = CnblogsItem()
            # 文章标题
            item['title'] = article.css('.titlelnk::text').extract_first()
            # 文章url
            item['url'] = article.css('.titlelnk::attr(href)').extract_first()
            # 文章作者
            item['author'] = article.css('.lightblue::text').extract_first()
            yield item
```

步骤04: 运行爬虫
```
scrapy crawl articles
```

#### 通用爬虫之XMLFeedSpider
步骤01: 创建项目
```
scrapy startproject xmlfeedspider
```

步骤02: 使用XMLFeedSpider模版创建爬虫
```
scrapy genspider -t xmlfeed jobbole jobbole.com
```

步骤03: 修改items.py
```
import scrapy

class JobboleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 文章标题
    title = scrapy.Field()
    # 发表日期
    public_date = scrapy.Field()
    # 文章链接
    link = scrapy.Field()
```

步骤04: 配置爬虫文件jobbole.py
```
# -*- coding: utf-8 -*-
from scrapy.spiders import XMLFeedSpider
# 导入item
from xmlfeedspider.items import JobboleItem

class JobboleSpider(XMLFeedSpider):
    name = 'jobbole'
    allowed_domains = ['jobbole.com']
    start_urls = ['http://top.jobbole.com/feed/']
    iterator = 'iternodes'  # 迭代器，不指定的话默认是iternodes
    itertag = 'item'  # 抓取item节点

    def parse_node(self, response, selector):
        item = JobboleItem()
        item['title'] = selector.css('title::text').extract_first()
        item['public_date'] = selector.css('pubDate::text').extract_first()
        item['link'] = selector.css('link::text').extract_first()
        return item
```