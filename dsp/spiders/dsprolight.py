# -*- coding: utf-8 -*-
import scrapy
from dsp.items import DspItem
import copy


class DsprolightSpider(scrapy.Spider):
    name = 'dsprolight'
    allowed_domains = ['www.dsprolight.com']
    start_urls = ['http://www.dsprolight.com/new-products.php']

    def parse(self, response):
        categorys = response.xpath('//*[@id="categories_block_left"]/ul/li/a')

        for cate in categorys:
            item = DspItem()
            item['cateUrl'] = cate.xpath('./@href').extract()[0]
            item['cateLongName'] = cate.xpath('./@title').extract()[0]
            item['cateName'] = cate.xpath('./text()').extract()[0]
            yield scrapy.Request("%s?n=100"%(item['cateUrl']),callback=self.parseProductList,meta={'item':item})


    def parseProductList(self,response):
        '''
        :type response: scrapy.http.response
        :param response:
        :return:
        '''
        productList = response.xpath("//div[@class='products clearfix']/ul/li")
        for product in productList:
            item = response.meta["item"]
            item['productUrl'] = product.xpath("./a/@href").extract()[0]
            item['productName'] = product.xpath("./a/@title").extract()[0]
            item['productImg'] = product.xpath("./a/img/@src").extract()[0]
            yield scrapy.Request("%s" % (item['productUrl']), callback=self.parseProductInfo, meta={'item': copy.deepcopy(item)})

    def parseProductInfo(self,response):
        '''
        :type response: scrapy.http.response
        :param response:
        :return:
        '''
        item = response.meta["item"]
        item['productImgList'] = response.xpath("//ul[@id='thumbs_list_frame']/li/a/@href").extract()
        item['productImg'] = response.xpath("//img[@id='bigpic']/@src").extract()[0]
        item['productInfo'] = response.xpath("//div[@class='more_info_block clearfix']")[0].extract()
        yield item



