# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


"""
实现保存分类的pipeline类
- open_spider 方法中，链接MongoDB数据库，获取要操作的集合
- process_item 方法中，向MongoDB中插入类别数据
- close_spider 方法中，关闭MongoDB的链接
"""
from pymongo import MongoClient
from jingDong.spiders.jd_category import JdCategorySpider
from jingDong.settings import MONGODB_URL


class CategoryPipeline(object):

    def open_spider(self, spider):
        """当爬虫启动的时候执行"""
        if isinstance(spider, JdCategorySpider):
            # open_spider方法中，链接MongoDB数据库，获取要操作的集合
            self.client = MongoClient(MONGODB_URL)
            self.collection = self.client['jd']['category']

    def process_item(self, item, spider):
        # process_item 方法中，想mongoDB中插入数据
        if isinstance(spider, JdCategorySpider):
            self.collection.insert_one(dict(item))

        return item

    def close_spider(self, spider):
        # close_spider 方法中，关闭MongoDB的连接
        if isinstance(spider, JdCategorySpider):
            self.client.close()


"""
8.1.实现存储商品Pipeline类
-在open_spider方法，建立MongoDB数据库连接，获取要操作的集合
-在process_item方法，把数据插入到MongoDB中
-在cLose_spider方法，关闭数据库连接

"""
from jingDong.spiders.jd_product import JdProductSpider


class ProductPipeline(object):

    def open_spider(self, spider):
        """当爬虫启动的时候执行"""
        if isinstance(spider, JdProductSpider):
            # open_spider方法中，链接MongoDB数据库，获取要操作的集合
            self.client = MongoClient(MONGODB_URL)
            self.collection = self.client['jd']['product']

    def process_item(self, item, spider):
        # process_item 方法中，想mongoDB中插入数据
        if isinstance(spider, JdProductSpider):
            self.collection.insert_one(dict(item))

        return item

    def close_spider(self, spider):
        # close_spider 方法中，关闭MongoDB的连接
        if isinstance(spider, JdProductSpider):
            self.client.close()