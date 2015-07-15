# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuestionItem(scrapy.Item):
    # define the fields for your item here like:
    qid = scrapy.Field()  # 问题id
    class_info = scrapy.Field()  # 问题分类
    ask_title = scrapy.Field()
    content = scrapy.Field()
    ask_time = scrapy.Field()  # 提问时间
    ask_tags = scrapy.Field()  # 问题tags标签，暂以 "," 分隔
    people_link = scrapy.Field()  # 提问人链接
    answers = scrapy.Field()


class AnswerItem(scrapy.Item):
    mode = scrapy.Field()  # 回答被分类型： 提问者采纳， 专业回答， 网友采纳， 普通回答
    pos_time = scrapy.Field()  # 回答时间
    content = scrapy.Field()
    people_link = scrapy.Field()  # 回答人链接


