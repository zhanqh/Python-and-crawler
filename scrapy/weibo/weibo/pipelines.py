# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class WeiboPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient('127.0.0.1', 27017)
        tdb = connection.scrapy
        self.post_info = tdb.weibo
    def process_item(self, item, spider):
        weibo = dict(item)
        self.post_info.insert(weibo)
        return item
