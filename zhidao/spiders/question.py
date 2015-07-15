# -*- coding: utf-8 -*-
import scrapy

from zhidao.items import QuestionItem, AnswerItem

class QuestionSpider(scrapy.Spider):
    name = "question"
    allowed_domains = ["zhidao.baidu.com"]
    start_urls = (
        "http://zhidao.baidu.com/question/%s.html" % s for s in range(143477925, 173070082)
    )

    def parse_answer(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        answer_list = []
        mode_xpath = response.selector.xpath('//section/article/div[contains(@class, mod-shadow)][2]//*[contains(@class, "title")]//text()').extract()
        if mode_xpath:
            # 如果存在特殊答案
            mode = mode_xpath[0]
            item = AnswerItem()
            item["mode"] = mode
            content = response.selector.xpath('//section/article/div[contains(@class, mod-shadow)][2]//*[contains(@class, "content")][1]').extract()
            item['content'] = content[0]
            people_xpath = response.selector.xpath('//section/article/div[contains(@class, mod-shadow)][2]//*[contains(@class, "name")]//@href').extract()
            item['people_link'] = people_xpath[0] if people_xpath else ""
            item['pos_time'] = response.selector.xpath('//section/article/div[contains(@class, mod-shadow)][2]//*[contains(@class, "time")]//text()').extract()[-1]
            answer_list.append(dict(item))
        else:
            mode = ""  # 其他普通回答
            common_list = response.selector.xpath('//section/article/div[contains(@id,"wgt-answers")]/div[2]/div[re:test(@id,"answer")]')
            for each in common_list:
                each_item = AnswerItem()
                each_item["people_link"] = each.xpath('div/div[1]/a/@href').extract()[0]  # 回答者link
                each_item["pos_time"] = each.xpath('div/div[1]/span/text()').extract()[1]  # 回答时间
                # 回答内容
                ls_qt_cntnt = each.xpath('div/div[2]/div[1]/span/text()').extract()
                each_item["content"] = "".join(ls_qt_cntnt)
                each_item["mode"] = mode
                answer_list.append(dict(each_item))
        return answer_list

    def parse(self, response):
        item = QuestionItem()
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        item["qid"] = response.url.split("/")[-1].split(".")[0]
        item["ask_title"] = response.selector.xpath('//section/article/div[contains(@id,"wgt-ask")]/h1/span/text()').extract()[0]  # 问题标题
        item["class_info"] = response.selector.xpath('//section/article/div[contains(@id,"wgt-ask")]/div[contains(@id,"ask-info")]/span[contains(@class,"classinfo")]/a/text()').extract()[0] # 问题分类
        item["ask_time"] = response.selector.xpath('//section/article/div[contains(@id,"wgt-ask")]/div[contains(@id,"ask-info")]/span/text()').extract()[0] #提问时间
        ask_person = response.selector.xpath('//section/article/div[contains(@id,"wgt-ask")]/div[contains(@id,"ask-info")]/a/text()').extract()
        # 提问者link
        if ask_person:
            people_link = response.selector.xpath('//section/article/div[contains(@id,"wgt-ask")]/div[contains(@id,"ask-info")]/a/@href').extract()[0]  # 提问者link
        else:
            people_link = ""  # 匿名

        item["people_link"] = people_link
        ask_tags_str = response.selector.xpath('//section/article/div[contains(@id,"wgt-ask")]/div[2]/span/text()').extract()
        if len(ask_tags_str) > 0:
            ask_tags = ask_tags_str[0]
        else:
            ask_tags = ""

        item["ask_tags"] = ask_tags
        ls_answer_cntnt = response.selector.xpath('//section/article/div[contains(@id,"wgt-ask")]/pre/text()').extract()
        item["content"] = "".join(ls_answer_cntnt)
        item["answers"] = self.parse_answer(response)
        return item

