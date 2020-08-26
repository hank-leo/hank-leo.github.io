---
title: Pandas异常值处理
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

### 生成异常数据
```
df=pd.DataFrame({'col1':[1,120,3,5,2,12,13],'col2':[12,17,31,53,22,32,43]})

#打印
print(df)
col1  col2  
0     1    12  
1   120    17  
2     3    31  
3     5    53  
4     2    22  
5    12    32  
6    13    43 
``` 

```
df_zscore=df.copy() #复制一个用来存储Z-score得分的数据框
cols=df.columns
for col in cols:
    df_col=df[col]
    z_score=(df_col - df_col.mean()) / df_col.std() #计算每列的Z-score得分
    df_zscore[col] = z_score.abs() > 2.2 #判断Z-score得分是否大于2.2,如果是则为True,否则为False

#打印，为True即异常值
print(df_zscore)
col1   col2  
0  False  False  
1   True  False  
2  False  False  
3  False  False  
4  False  False  
5  False  False  
6  False  False  
```

### 获取无异常值的数据
```
df_drop_outlier=df[df_zscore['col1']==False]

print(df_drop_outlier)
col1  col2  
0     1    12  
2     3    31  
3     5    53  
4     2    22  
5    12    32  
6    13    43  
```