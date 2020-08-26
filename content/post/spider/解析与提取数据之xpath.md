---
title: "解析与提取数据之xpath"
date: 2019-12-06
draft: false
tags: ["xpath"]
categories: ["爬虫学习"]
---

日常工作主要使用xpath进行数据的解析和提取，归于xpath有着强大的功能，适应大多数的网页结构。

```
#导入包
from lxml import etree

def get_data(response):
    html=etree.HTML(response)
    #提取属性值
    url=html.xpath("//div[@href]")
    #提取文本
    title=html.xpath("//div[@class='title']/text()")
```