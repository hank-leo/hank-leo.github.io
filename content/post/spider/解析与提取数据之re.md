---
title: "解析与提取数据之re"
date: 2019-12-06
draft: false
tags: ["re"]
categories: ["爬虫学习"]
---

对比xpath, re对文本结构的数据处理更加灵活
```
#导入包
import re

def get_data(response):
    #提取内容
    title = re.findall("^<span>(.*?)</span>",response, re.S)
```
