# -*- coding: utf-8 -*-
from urllib import request

import scrapy
from scrapy import Request

from ..items import NutItem


class TechSpider(scrapy.Spider):
    name = 'tech'
    allowed_domains = ['www.tech-food.com']
    start_urls = ['https://www.tech-food.com/kndata/d21']

    def parse(self, response):
        authors_urls = response.xpath("//div[@class='titleTxt']/a/@href").extract()
        for authors_url in authors_urls:
            authors_url = "https://www.tech-food.com" + authors_url
            yield Request(authors_url, callback=self.author_callback)

        next_urls = response.xpath("//div[@class='Listmore_title4'][1]/a/@href").extract()[0:10]
        for next_url in next_urls:
            next = "https://www.tech-food.com" + next_url
            yield Request(next,callback=self.parse)


    # def next(self, response):
    #     print("***********3****")
    #     next_urls = response.xpath("//div[@class='Listmore_title4'][1]/a/@href").extract()
    #     print(next_urls,"^^^^^^^^^^^^^^^^")
    #     print(next_urls, "*********6********")
    #     for next_url in next_urls:
    #         next = "https://www.tech-food.com" + next_url
    #         print(next,"%%%%%%%%%%%%")
    #         print("****发送****")
    #         yield Request(next, callback=self.parse)


    def author_callback(self,response):
        names = response.xpath("//div[@class='biaoti1']/h1/text()").extract()[0]
        texts = response.xpath("//div[@id='zoom']/p[1]/text()").extract()[0]
        img_urls = response.xpath("//div[@id='zoom']/p[2]/img/@src").extract()[0]


        nut_item = NutItem()
        nut_item["title"] = names
        nut_item["content"] = texts
        nut_item["content_img"] = img_urls
        yield nut_item


    #     next_urls = response.xpath("//div[@class='Listmore_title4'][1]/a[11]/@href").extract()
    #     for next in next_urls:
    #         n_urls = "https://www.tech-food.com"+next
    #         print(n_urls,"******55555********")
    #         yield Request(n_urls,callback=self.current)
    #
    # def current(self,response):
    #     author_urls = response.xpath("//div[@class='titleTxt']/a/@href").extract()
    #     for author_url in author_urls:
    #         url = "https://www.tech-food.com"+author_url
    #         print(url,"********6********")
    #         yield Request(url,callable=self.get_nut)
    #
    #
    # def get_nut(self,response):
    #     title = response.xpath("//div[@class='biaoti1']/h1/text()")
    #     paragraph = response.xpath("//div[@id='zoom']/p[1]/text()")
    #     img_urls = response.xpath("//div[@id='zoom']/p[2]/img/@src")
    #     nut_item = NutItem()
    #     nut_item["title"] = title
    #     nut_item["paragraph"] = paragraph
    #     nut_item["img_urls"] = img_urls
    #     yield nut_item


    # def call_back(self,response):
        # author_urls = response.xpath("//ul/li/div[@class='Describe']")
        # for author_url in author_urls:
        #     texts= author_url.xpath(".//text()").extract()
        #     text = texts[0]
        #     alt_name = author_url.xpath(".//div[@class='titletu']/a/img/@alt").extract()
        #     name = alt_name[0]
        #     img_urls = author_url.xpath(".//div[@class='titletu']/a/img/@src").extract()
        #     img_url = img_urls[0]
        #     request.urlretrieve(img_url,filename="D:\\PyCharm\\PyCharmwrok\\Nutrition\\Nut\\Nut\\imgs\\"+name+'.jpg')
        #     # titles = open("title.txt",'a',encoding="utf-8")
        #     # titles.write(name+'\n')
        #     # titles.write(text + '\n\n')
        #     print(name+"下载成功")
        #
        #     nexts_page = response.xpath("//div[@class='Listmore_title4'][1]/a[11]/@href").extract()
        #     for nexts in nexts_page[0:10]:
        #         next = "https://www.tech-food.com" + nexts
        #         print(next)
        #         yield Request(next, callback=self.parse)

# def parse(self,response):
    #     print("***********3****")
    #     next_urls = response.xpath("//div[@class='Listmore_title4'][1]/a/@href").extract()
    #     print(next_urls,"*********6********")
    #     print("######4########")
    #     if next_urls:
    #         print("*****5*****")
    #         for next_url in next_urls:
    #             next_url = next_url[0]
    #             next = "https://www.tech-food.com" + next_url
    #             print("****发送****")
    #             yield Request(next,callback=self.dang)