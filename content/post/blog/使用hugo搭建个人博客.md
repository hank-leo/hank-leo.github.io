---
title: "使用hugo搭建个人博客"
date: 2019-12-05
draft: false
tags: ["hugo"]
categories: ["博客搭建"]
---

### 安装
在这个页面下载安装https://github.com/gohugoio/hugo/releases

下载完成后解压，将解压出来的可执行文件，放到自定义目录下，并将选择的路径放入环境变量path中


### 初始化
下面开始存放我们的博客，在选好的路径下执行
```
hugo new site ihankleo.github.io
```

命令执行完会创建一个名为myBlog(自定义)的文件夹来存放博客相关文件内容

进入ihankleo.github.io下的目录结构应该是这样的
```
├── archetypes # 内容类型，在创建新内容时自动生成内容的配置
├── content # 网站内容，Markdown 文件
├── data
├── layouts # 网站模版，选择主题后会将主题中的 layouts 文件夹中的内容复制到此文件夹中
├── static # 包含 CSS、JavaScript、Fonts、media 等，决定网站的外观。选择主题后会将主题中的 ststic 文件夹中的内容复制到此文件夹中
├── themes # 存放主题文件
└── config.toml # 网站的配置文件
```

### 安装主题

在博客根目录下执行
```
git clone https://github.com/xianmin/hugo-theme-jane.git --depth=1 themes/jane
```

### 创建新页面
```
hugo new about.md
```

此时```content```文件夹下回多一个```about.md```文件
打开文件，内容如下
```
---
title: "About"
date: 2019-12-04T17:49:25+08:00
draft: true
---

```

两条 --- 间的信息是文章的配置信息，有的信息是自动生成的 (如：title、date 等)，简单介绍以下各项配置

以下项目是自动生成的:
```
title: # 文章标题
date: # 写作时间
draft: # 是否为草稿，如果为 true 需要在命令中加入 --buildDrafts 参数才会生成这个文档
```


以下项目需要自行添加:
```
description: # 描述
tags: # 标签，用于文章分类
```

自动生成 和 执行添加 的内容并不是绝对的，你可以根据自己的喜好配置模板文件```archetypes/default.md```

### 配置 ```config.toml```

用于存放整个网站的配置信息
```
# This is a simple configuration.
# If you want to see the full configuration, please check `full-config.toml` .
# And see https://gohugo.io/getting-started/configuration/ .

baseURL = "https://ihankleo.github.io"
title = "Hank's Blog"
enableRobotsTXT = true
enableEmoji = true
theme = "jane"

hasCJKLanguage = true     # has chinese/japanese/korean ? # 自动检测是否包含 中文\日文\韩文
paginate = 5              # Number of articles displayed on the homepage  # 首页每页显示的文章数
rssLimit = 20             # Limit Entry Count to Rss file # 限制 Rss 文章输出数量
disqusShortname = ""      # disqus_shortname
googleAnalytics = ""      # UA-XXXXXXXX-X
copyright = ""            # default: author.name ↓        # 默认为下面配置的author.name ↓

# language support # en / zh-cn / other... translations present in i18n/
defaultContentLanguage = "zh-cn"           # Default language to use
[languages.zh-cn]
  languageCode = "zh-cn"

[author]                  # essential                     # 必需
  name = "Hank"

[sitemap]                 # essential                     # 必需
  changefreq = "weekly"
  priority = 0.5
  filename = "sitemap.xml"

[[menu.main]]             # config your menu              # 配置目录
  name = "主页"
  weight = 10
  identifier = "home"
  url = "/"
[[menu.main]]
  name = "归档"
  weight = 20
  identifier = "archives"
  url = "/post/"
[[menu.main]]
  name = "标签"
  weight = 20
  identifier = "tags"
  url = "/tags/"
[[menu.main]]
  name = "分类"
  weight = 20
  identifier = "categories"
  url = "/categories/"
[[menu.main]]
  name = "Github"
  weight = 30
  url = "https://ihankleo.github.io"


[params]
  since = "2019"            # Site creation time          # 站点建立时间
  homeFullContent = false   # if false, show post summaries on home page. Othewise show full content.
  rssFullContent = true     # if false, Rss feed instead of the summary

  # site info (optional)                                  # 站点信息（可选，不需要的可以直接注释掉）
  logoTitle = "Hank's Blog"        # default: the title value    # 默认值: 上面设置的title值
  keywords = ["Hugo", "theme","jane"]
  description = "Just Gan It"

  # The date format to use; for a list of valid formats, see https://gohugo.io/functions/format/
  dateFormatToUse = "2006-01-02"

  # 一些全局开关，你也可以在每一篇内容的 front matter 中针对单篇内容关闭或开启某些功能，在 archetypes/default.md 查看更多信息。
  # Some global options, you can also close or open something in front matter for a single post, see more information from `archetypes/default.md`.
  toc = true                                                                            # 是否开启目录
  photoswipe = true         # see https://github.com/dimsemenov/PhotoSwipe            # 是否启用PhotoSwipe（图片可点击）
  contentCopyright = '<a rel="license noopener" href="https://creativecommons.org/licenses/by-nc-nd/4.0/" target="_blank">CC BY-NC-ND 4.0</a>'

  # Link custom CSS and JS assets
  #   (relative to /static/css and /static/js respectively)
  customCSS = []            # if ['custom.css'], load '/static/css/custom.css' file
  customJS = []             # if ['custom.js'], load '/static/js/custom.js' file

```

### 生成网站

设置完成后执行命令
```
hugo server --buildDrafts -w
```

参数介绍

- buildDrafts: 生成被标记为 「草稿」 的文档

- w: 监控更改，如果发生更改直接显示到博客上 (非常有用，这也是我最喜欢的一点特性了)


此时可以通过```http://localhost:1313```访问本地博客了


但此时只能在本地访问 (相当于预览博客，如果与期望值不符，可以随时更改)，

如果想发布到 Github Pages 上需要先将文章配置信息中的```draft:```改为```false```然后执行命令
```
hugo
```

此时你的博客目录下会多出一个 public 文件夹来。这便是 Hugo 生成的网站

### 发布

不像 Hexo，Hugo 并没有提供自动发布到 GitHub Pages 的功能。需要将 public 中的内容手动上传到 Github 上。

首先执行命令```cd public``` 进入到 ```public``` 文件夹中 然后执行
```
git init
git remote add origin https://github.com/[Github 用户名]/[Github 用户名].github.io.git
git add -A
git commit -m "[介绍，随便写点什么，比如日期]"
git push -u origin master
```

第一次发布需要执行的命令多一点，以后发布只需要执行
```
git add -A
git commit -m "[介绍，随便写点什么，比如日期]"
git push -u origin master
```

#### 一键发布博客

通过配置文件deploy.sh实现一键部署到GitHub
* deploy.sh文件放在站点根目录下；
- 执行方法分两种（windows下）：

方法一：站点根目录下，鼠标右键，打开git bash here窗口，执行sh deploy.sh。
方法二：选中deploy.sh文件，鼠标右键属性，更改打开方式，将打开方式选择为git-bash.exe执行文件，以后写新的文章后，双击下脚本文件即可成功推送到github上
```
#!/bin/bash

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"

# Build the project.
hugo # if using a theme, replace by `hugo -t <yourtheme>`

# Go To Public folder
cd public
# Add changes to git.
git add -A

# Commit changes.
msg="rebuilding site `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit -m "$msg"

# Push source and build repos.
git push origin master

# Come Back
cd ..
```

----



### 遇到的报错

**git 无法push远程仓库 Note about fast-forwards**

分析：

此项错误是由于本地仓库和远程有不同的开始点，也就是两个仓库没有共同的 commit 出现的无法提交。这里我们需要用到 `--allow-unrelated-histories`。也就是我们的 pull 命令改为下面这样的： 

解决：

```
git pull origin master --allow-unrelated-histories
```

或者

```
git push -f origin master
```
