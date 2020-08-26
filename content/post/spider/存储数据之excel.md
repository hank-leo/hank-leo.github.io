---
title: "存储数据之excel"
date: 2019-12-06
draft: false
tags: ["excel"]
categories: ["爬虫学习"]
---

* 第一种方式是使用pandas库
```
def save(data):
    data = pd.DataFrame(data)
    data.to_excel(index=False)
```

* 第二种方式是使用openpyxl库
```
import openpyxl
def save(title, head, data):
    outwb = openpyxl.Workbook()
    outws = outwb.active
    outws.title=title
    for h in range(len(head)):
        outws.cell(1,h+1).value=head[h]
    for row in data:
        outws.append(row)
    outwb.save("path")
```

* 第三种方式是使用xlwt库
```
def save(title, head, data):
    workbook = xlwt.Workbook(encoding='utf8')
    sheet = workbook.add_sheet(title, cell_overwrite_ok=True)
    for h in range(len(head)):
        sheet.write(0, h, head[h])
    i = 1
    for list in data:
        j = 0
        for data in list:
            sheet.write(i, j, data)
            j += 1
        i += 1
    workbook.save(path)
```
