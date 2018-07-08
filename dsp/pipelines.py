# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy,MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
from scrapy.contrib.pipeline.images import ImagesPipeline
from datetime import datetime
from scrapy import log
import util

def toStr(str):
    if isinstance(str,list) or isinstance(str,tuple):
        return  ''.join(str)
    else:
        return str

class DspImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return "full/%s"%(image_guid)

    def get_media_requests(self, item, info):
        yield scrapy.Request(item["productImg"])

    def item_completed(self, results, item, info):
        image_paths = ["../upload/%s/%s"%(datetime.now().strftime("%Y%m"),x['path']) for ok, x in results if ok]
        if len(image_paths) > 0:
            item['productImg'] = image_paths[0]
        return item

class DspImageListPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return "full/%s"%(image_guid)

    def get_media_requests(self, item, info):
        for imageurl in item['productImgList']:
            yield scrapy.Request(imageurl)

    def item_completed(self, results, item, info):
        image_paths = ["../upload/%s/%s"%(datetime.now().strftime("%Y%m"),x['path']) for ok, x in results if ok]
        item['productImgList'] = image_paths
        return item


class DspPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # 从配置中获取信息
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入编程异步执行
        # 第一个参数是我们定义的函数
        query = self.dbpool.runInteraction(self.do_insert, item)

        return item

        # 错误处理函数

    def handle_error(self, falure):
        print(falure)

    def get_displayimg(self,productName,imglist):
        if len(imglist) == 0:
            return ''
        else:
            return "|".join([productName+"*"+img+"*150x150" for img in imglist])

    def do_insert(self, cursor, item):
        """
        :param cursor: MySQLdb.cursors.Cursor
        :param item:
        :return:
        """
        top_cate_sql = "select * from met_column where bigclass = '0' and name = 'product'"
        cursor.execute(top_cate_sql)
        top_cate_row = cursor.fetchone()
        if top_cate_row is None:
            raise Exception("no top category name product")

        cate_where_str = "bigclass = '%d' and name='%s'"%(top_cate_row['id'],item['cateName'])
        cate_update_data = {
            'keywords':item['cateLongName'],
            'name':item['cateName']
        }
        cate_insert_data = {
            'keywords': item['cateLongName'],
            'name': item['cateName'],
            'foldername':'product',
            'bigclass':top_cate_row['id'],
            'module':'3',
            'list_order':'1',
            'classtype':'2',
            'isshow':'1',
            'lang':'en'
        }

        #更新分类
        cate_row = util.insert_or_update(cursor,'met_column',cate_where_str,cate_insert_data,cate_update_data)

        product_where_str = "title='%s'"%(item['productName'],)
        displayimg = self.get_displayimg(item['productName'], item['productImgList'])
        product_insert_data = {
            'title': item['productName'],
            'description':item['cateLongName'],
            'content':item['productInfo'],
            'imgurl':item['productImg'],
            'class1':top_cate_row['id'],
            'class2':cate_row['id'],
            'lang':'en',
            'addtime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'updatetime':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'displayimg':displayimg
        }
        product_update_data = {
            'description': item['cateLongName'],
            'content': item['productInfo'],
            'imgurl': item['productImg'],
            'class1': top_cate_row['id'],
            'class2': cate_row['id'],
            'updatetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'displayimg': displayimg
        }

        # 更新产品
        util.insert_or_update(cursor, 'met_product', product_where_str, product_insert_data, product_update_data)