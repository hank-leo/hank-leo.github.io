---
title: Pandas重复值处理
date: 2019-12-04
draft: false
keywords: ["pandas"]
description: ""
tags: ["pandas"]
categories: ["Pandas学习"]
author: ""
---

**导包**
```
import pandas as pd
```

### 生成数据
```
data1,data2,data3,data4=['a',3],['b',2],['a',3],['c',2]
df=pd.DataFrame([data1,data2,data3,data4],columns=['col1','col2'])
print(df)
```
> col1  col2  
0    a     3  
1    b     2  
2    a     3  
3    c     2  


### 判断数据
```
isDuplicated=df.duplicated() #判断重复数据记录
print(isDuplicated)
```
> 0    False  
1    False  
2     True  
3    False  
dtype: bool


### 删除重复的数据
```
print(df.drop_duplicates()) #删除所有列值相同的记录，index为2的记录行被删除
```
> col1  col2  
0    a     3  
1    b     2  
3    c     2  


```
#删除col1列值相同的记录，index为2的记录行被删除
print(df.drop_duplicates(['col1'])) 
```
> col1  col2  
0    a     3  
1    b     2  
3    c     2  


```
#删除col2列值相同的记录，index为2和3的记录行被删除
print(df.drop_duplicates(['col2'])) 
```
> col1  col2  
0    a     3  
1    b     2  


```
#删除指定列（col1和col2）值相同的记录，index为2的记录行被删除
print(df.drop_duplicates(['col1','col2'])) 
```
> col1  col2  
0    a     3  
1    b     2  
3    c     2  

