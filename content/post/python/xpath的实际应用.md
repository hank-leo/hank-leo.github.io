---
title: "Xpath的实际应用"
date: 2019-12-05
draft: false
tags: ["xpath"]
categories: ["Python实际应用"]
---

#### xpath中使用contains
```
xpath(span[contanins(@class, 'xxx')])
```
Xpath如何选择不包含某一个属性的节点?
这里可以用到 not 例如排除一个属性的节点可以使用
```
//tbody/tr[not(@class)]
```

排除一个或者两个属性可以使用
```
//tbody/tr[not(@class or @id)]
```

#### xpath按序选择
有时候我们在选择的时候可能某些属性同时匹配了多个节点，但是我们只想要其中的某个节点，如第二个节点，或者最后一个节点，这时该怎么办呢？

这时可以利用中括号传入索引的方法获取特定次序的节点，示例如下：
```
from lxml import etree
text = '''
first item
second item
third item
fourth item
fifth item
'''
html = etree.HTML(text)
result = html.xpath('//li[1]/a/text()')
print(result)
result = html.xpath('//li[last()]/a/text()')
print(result)
result = html.xpath('//li[position()<3]/a/text()')
print(result)
result = html.xpath('//li[last()-2]/a/text()')
print(result)
```
第一次选择我们选取了第一个 li 节点，中括号中传入数字1即可，注意这里和代码中不同，序号是以 1 开头的，不是 0 开头的。 第二次选择我们选取了最后一个 li 节点，中括号中传入 last() 即可，返回的便是最后一个 li 节点。 第三次选择我们选取了位置小于 3 的 li 节点，也就是位置序号为 1 和 2 的节点，得到的结果就是前 2 个 li 节点。 第四次选择我们选取了倒数第三个 li 节点，中括号中传入 last()-2即可，因为 last() 是最后一个，所以 last()-2 就是倒数第三个。

运行结果如下：
```
['first item']
['fifth item']
['first item', 'second item']
['third item']
```
在这里我们使用了 last()、position() 等函数，XPath 中提供了 100 多个函数，包括存取、数值、字符串、逻辑、节点、序列等处理功能。 具体所有的函数作用可以参考：http://www.w3school.com.cn/xpath/xpath_functions.asp。

#### xpath获取带注释的text
```
from lxml import etree

html_str = """
this from blog.csdn.net/lncxydjq , DO NOT COPY!
*****
html = etree.HTML(html_str)
print html.xpath('//div[@id="box1"]/div/node()')[1]
print type(html.xpath('//div[@id="box1"]/div/node()')[1])
print html.xpath('//div[@id="box1"]/div/node()')[1].text
```

output:
```
can u get me, bitch?
```