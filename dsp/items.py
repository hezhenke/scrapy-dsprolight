# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DspItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cateUrl = scrapy.Field()
    cateName = scrapy.Field()
    cateLongName = scrapy.Field()
    productUrl = scrapy.Field()
    productName = scrapy.Field()
    productImg = scrapy.Field()
    productImgList = scrapy.Field()
    productInfo = scrapy.Field()
