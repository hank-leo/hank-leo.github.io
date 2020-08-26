---
title: 'Scrapy框架:Request回调函数'
date: 2019-12-04
draft: false
tags: ["Scrapy"]
categories: ["Scrapy框架学习"]
---
**Request回调函数**
```
def parse_page1(self, response):
    return scrapy.Request("http://www.example.com/some_page.html",
                          callback=self.parse_page2)

def parse_page2(self, response):
    # this would log http://www.example.com/some_page.html
    self.logger.info("Visited %s", response.url)
```

**传递参数**
```
def parse_page1(self, response):
    item = MyItem()
    item['name'] = response.css('.name::text').extract_first()
    request = scrapy.Request("http://www.example.com/some_page.html",
                             callback=self.parse_page2)
    request.meta['item'] = item
    yield request

def parse_page2(self, response):
    item = response.meta['item']
    item['age'] = response.css('.age::text').extract_first()
    yield item
```