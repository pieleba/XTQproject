# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FoodsinfoItem(scrapy.Item):
    fid = scrapy.Field()
    fname = scrapy.Field()
    fimg = scrapy.Field()
    fpopnum = scrapy.Field()
    fprice = scrapy.Field()
    fcategory = scrapy.Field()
    fstorenum = scrapy.Field()