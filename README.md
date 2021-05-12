# quncloud
基于graia的一个qq群词云生成器

## 依赖安装

wordcloud

`pip install wordcloud`

jieba


`pip install jieba`


arrow

`pip install arrow`

## 用法
在群里请求的格式
`/云图 ` 默认输出当天的云图
`/云图 [年|月|日] [n(数字)|None] ` 输出n(年|月|日)前的云图信息，不输入数字或输入0代表 当前（年月日）信息

`/云图 精确 YYYY MM DD ` 查找具体日期下的云图信息

`/云图 屏蔽词 str1 str2 ...` 添加当前群的屏蔽词

`/云图 屏蔽词 全局 str1 str2 ...` 添加全局屏蔽词

## 例子

`/云图 日期 1` 生成昨天当天的词云图

`/云图 月份 1` 生成上个月整个月的词云图

`/云图 精确 2021 5 1` 生成2021年五月1日的日期

## 杂项

1. 可以在stopwords.txt 添加屏蔽词（我用的是网上随便找的百度的？
2. a.png 是背景图可以自己换
3. 第一次用github随便写给朋友看的轻喷
