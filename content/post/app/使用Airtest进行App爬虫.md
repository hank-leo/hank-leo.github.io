---
title: "使用Airtest进行App爬虫"
date: 2019-12-06
draft: false
tags: ["airtest","爬虫"]
categories: ["App爬虫"]
---

### 前言
Airtest是网易开发的手机UI戒面自动化测试工具，

### 安装
从[Airtest官网](https://airtest.netease.com) : https://airtest.netease.com   下载Airtest，然后像安装普通软件一样安装即可。

### 手机连接

启动Airtest以后，把Android手机连接到电脑上，点击下图方框中的**refresh ADB**

然后点击connect按钮

### 开始爬虫
以某品牌咖啡的app为例子

#### 输入文字
在输入框发送文字
```
poco(name="cn.com.coffee:id/cp_search_box").set_text()
```

#### 选择文本
```
poco(name='cn.com.coffee:id/tv_store_name').get_text()
```

#### 点击元素
```
poco(name="cn.com.coffee:id/cp_list_item_name").click()
```

### 最后
这里简单介绍使用Airtest进行App的爬虫，更多知识点可参考：

[Airtest官网文档](http://airtest.netease.com/docs/cn/index.html) : http://airtest.netease.com/docs/cn/index.html

[Poco官网文档](https://poco.readthedocs.io/zh_CN/latest/) : https://poco.readthedocs.io/zh_CN/latest/
