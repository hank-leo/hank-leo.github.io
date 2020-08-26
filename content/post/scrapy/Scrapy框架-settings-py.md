---
title: 'Scrapy框架:Settings.py'
date: 2019-12-04
draft: false
tags: ["Scrapy"]
categories: ["Scrapy框架学习"]
---
```
#Scrapy项目名字
BOT_NAME = 'segmentfault'

#Scrapy搜索spider的模块列表
SPIDER_MODULES = ['segmentfault.spiders']

#使用爬虫创建命令genspider创建爬虫时生成的模块
NEWSPIDER_MODULE = 'segmentfault.spiders'

#默认的USER_AGENT, 使用BOT_NAME配置生成，建议覆盖
#USER_AGNET = 'segmentfault (+http://www.yourdomain.com)'

#如果启用，Scrapy则会遵守网站Rebots.txt协议，建议设置为False
ROBOTSTXT_OBEY = True

#配置Scrapy最大并发数，默认为32，一般需要增大设置
CONCURRENT_REQUESTS = 32

#为同一个站点设置下载延迟
DOWNLOAD_DELAY = 3

#下载延迟的设置只会根据以下两个中的一个生效
#对单个网站设置最大的请求并发数
#CONCURRENT_REQUESTS_PER_DOMAIN = 16

#对单个IP设置最大的请求并发数
#CONCURRENT_REQUESTS_PER_IP = 16

#禁用Cookie, 默认True启用，建议为False
#COOKIES_ENABLED = False

#关闭Telent控制台，默认启用
#TELNETCONSOLE_ENABLED = False

#默认的请求头，根据爬取网站覆盖
#DEFAULT_REQUEST_HEADERS = {
#    'Accept': '',
#    'Accept-Language': 'en',
#}

#启用Spider爬虫中间件
#SPIDER_MIDDLEWARES = {
#    'segmentfault.middlewares.SegmentfaultSpiderMiddleware': 543,
#}

#启用Downloader下载器中间件
#DOWNLOADER_MIDDLEWARES = {
#    'segmentfault.middlewares.SegmentfaultDownloaderMiddleware': 543,
#}

#启用扩展
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

#配置管道信息
#ITEM_PIPELINES = {
#    'segmentfault.pipelines.SegmentfaultPipeline': 300,
#}

#启用配置AutoThrottle扩展，默认禁用，建议启用
#AUTOTHROTTLE_ENABLED = True

#初始化下载延迟
#AUTOTHROTTLE_START_DELAY = 5

#高延迟下最大的下载延迟
#AUTOTHROTTLE_MAX_DELAY = 60

#Scrapy请求应该并行发送每个远程服务器的平均数量
#AUTOTHROTTLE_TARGENT_CONCURRENCY = 1.0

#启用调试模式，统计每一个响应状态数据
#AUTOTHROTTLE_DEBUG = False

#启用和配置HTTP缓存
#HTTPCACHE_ENABLED = True

#HTTP缓存目录
HTTPCHCHE_DIR = 'httpcache'

#HTTP缓存忽略的响应状态码
HTTPCACHE_IGNORE_HTTP_CODES = []

#HTTP缓存存储目录
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
```
