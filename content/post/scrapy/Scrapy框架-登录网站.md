---
title: "Scrapy框架 登录网站"
date: 2019-12-04
draft: false
tags: ["Scrapy"]
categories: ["Scrapy框架学习"]
---

### 使用cookies登录网站
```
import scrapy

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['xxx.com']
    start_urls = ['https://www.xxx.com/xx/']

    cookies = ""

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        with open("01login.html", "wb") as f:
            f.write(response.body)

```


### 发送post请求登录, 要手动解析网页获取登录参数
```
import scrapy

class LoginSpider(scrapy.Spider):
    name='login_code'
    allowed_domains = ['xxx.com']
    
    #1. 登录页面
    start_urls = ['https://www.xxx.com/login/']

    def parse(self, response):
        #2. 代码登录
        login_url='https://www.xxx.com/login'

        formdata={
            "username":"xxx",
            "pwd":"xxx",
            "formhash":response.xpath("//input[@id='formhash']/@value").extract_first(),
            "backurl":response.xpath("//input[@id='backurl']/@value").extract_first()
        }

        #3. 发送登录请求post
        yield scrapy.FormRequest(login_url, formdata=formdata, callback=self.parse_login)
    
    def parse_login(self, response):
        #4.访问目标页面
        member_url="https://www.xxx.com/member"
        yield scrapy.Request(member_url, callback=self.parse_member)
    
    def parse_member(self, response):
        with open("02login.html",'wb') as f:
            f.write(response.body)

```


### 发送post请求登录, 自动解析网页获取登录参数
```
import scrapy

class LoginSpider(scrapy.Spider):
    name='login_code2'
    allowed_domains = ['xxx.com']
    
    #1. 登录页面
    start_urls = ['https://www.xxx.com/login/']

    def parse(self, response):
        #2. 代码登录
        login_url='https://www.xxx.com/login'

        formdata={
            "username":"xxx",
            "pwd":"xxx"
        }

        #3. 发送登录请求post
        yield scrapy.FormRequest.from_response(
            response,
            formxpath="//*[@id='login_pc']",
            formdata=formdata,
            method="POST", #覆盖之前的get请求
            callback=self.parse_login
        )
    
    def parse_login(self, response):
        #4.访问目标页面
        member_url="https://www.xxx.com/member"
        yield scrapy.Request(member_url, callback=self.parse_member)
    
    def parse_member(self, response):
        with open("03login.html",'wb') as f:
            f.write(response.body)
```

### 实战1: 使用FormRequest模拟登录豆瓣
**创建项目**
```
scrapy startproject douban
```

**创建爬虫**
```
scrapy genspider login douban.com
```

#### 编写login.py
```
# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import FormRequest

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['douban.com']
    start_urls = ['https://www.douban.com/']

    # 请求头信息，豆瓣会禁止Scrapy默认的头信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # 使用FormRequests发送请求，指定URL、请求头信息、请求参数、回调函数
    def start_requests(self):
        return [FormRequest(url='https://accounts.douban.com/j/mobile/login/basic',
                            headers=self.headers,
                            # 表单数据
                            formdata={'name': '1120844583@qq.com',
                                      'password': 'guoqing110',
                                      'remember': 'false'},
                            # 回调函数
                            callback=self.login_check)]

    # 检查登录状态，登录成功后回调爬虫处理函数
    def login_check(self, response):
        if "failed" not in response.text:
            # 登录成功，请求start_url中url
            for url in self.start_urls:
                yield scrapy.Request(url=url,
                                     headers=self.headers,
                                     callback=self.parse)
        else:
            # 登录失败，则提取失败描述信息
            data = json.loads(response.text)
            self.logger.info(data['description'])

    # 爬虫处理函数
    def parse(self, response):
        user_check = response.css('.nav-user-account > a > span::text').extract_first()
        self.logger.info('{}已经登录成功'.format(user_check))
```

#### 编写settings.py
```
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
```

### 实战2: 使用Cookie登录

新建爬虫文件loginwithcookie.py
```
# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest

class LoginwithcookieSpider(scrapy.Spider):
    name = 'loginwithcookie'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']

    cookies = {
		'__yadk_uid':'r1ui3ZQLIms2rcKxGyeNwLmzc8lUPH63',
		'_pk_id.100001.8cb4':'b74b50748759cfae.1548945951.5.1552140943.1549757800.',
		'_pk_ses.100001.8cb4':'*',
		'_vwo_uuid_v2':'D64CD4759E8B751D295BF6BB8C0A17D49|9bc14c89ac7c1fa5caf93699bc6283e7',
		'bid':'XzwxkKpWlcU',
		'dbcl2':'"190816154:EUPQ9myKid0"',
		'douban-profile-remind':'1',
		'gr_user_id':'7a61a89a-323b-45ca-9218-5029810ba568',
		'll':'"118282"',
		'push_doumail_num':'0',
		'push_noty_num':'0',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xm…plication/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language':	'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Host': 'book.douban.com',
        'Referer': 'https://www.douban.com/people/sugermaster/',
        'Upgrade-Insecure-Requests': '1',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0"

}

    # 使用FormRequests发送请求，指定url，请求头信息，cookies
    def start_requests(self):
        for url in self.start_urls:
            return [FormRequest(url,
                                headers=self.headers,
                                # formdata={'name': '1120844583@qq.com',
                                #           'password': 'guoqing1010',
                                #           'remember': 'false'},
                                cookies=self.cookies,
                                callback=self.parse)]

    # 爬虫处理函数
    def parse(self, response):
        user_check = response.css(
            '.nav-user-account > a > span::text').extract_first()
        self.logger.info('{}已经登录成功'.format(user_check))
```