# -*- coding: utf-8 -*-

import random
import scrapy
from scrapy import Request

from ..items import FoodsinfoItem


class MhjSpider(scrapy.Spider):
    name = 'msj'
    allowed_domains = ['www.meishij.net']
    start_urls = ['http://www.meishij.net/chufang/diy/']

    def parse(self, response):
        for type_url in response.xpath("//div[@class='main']//li//a/@href").extract()[1:4]:
            type_url = "https://www.meishij.net"+type_url
            yield Request(type_url, callback=self.type_food)

    def type_food(self, response):
        for page_url in response.xpath("//div[@class='listtyle1_page']//a/@href").extract()[0:2]:
            yield Request(page_url, callback=self.get_foods_info)

    def get_foods_info(self, response):

        for food_url in response.xpath("//div[@class='listtyle1']"):
            category = response.xpath("//div[@class='listtyle1_page']//a/@href").extract()[0].split('/')[-2]
            food_item = FoodsinfoItem()
            img_url = food_url.xpath(".//a[@target='_blank']/img/@src").extract()[0]
            # imgname = img_url.split('/')[-1]
            # request.urlretrieve(img_url, filename="D:\\PyCharm\\scrapy_foods\\foodsinfo\\foodsinfo\\imgs\\" + imgname)
            # print("===========", "图片下载完毕！")
            foodname = food_url.xpath(".//div[@class='c1']/strong/text()").extract()[0]
            foodpop = food_url.xpath(".//div[@class='c1']/span/text()").extract()[0].split(' ')[-2]
            # with open('../title.txt','a') as f:
            #             #     f.write(imgname+"\t"+title+"\t"+pop+'\n')
            #             # print("+++++++++++++++++++++","数据已保存！")
            error_data = ['东北蘸酱菜 营养省事又爽口', '香草芭菲', '下酒小凉菜-改良版口水鸡丝']
            if foodname not in error_data:
                fprice = random.randint(20, 40)
                storenum = random.randint(5,20)
                if category == 'caixi':
                    category = '中华菜系'
                    food_item['fcategory'] = category
                elif category == 'xiaochi':
                    category = '各地小吃'
                    food_item['fcategory'] = category
                # elif category == 'guowaicaipu1':
                else:
                    category = '国外菜谱'
                    food_item['fcategory'] = category
                food_item['fname'] = foodname
                food_item['fimg'] = img_url
                food_item['fpopnum'] = int(foodpop)
                food_item['fprice'] = fprice
                food_item['fstorenum'] = storenum
                print("food_item的内容是------------>",food_item)
                yield food_item