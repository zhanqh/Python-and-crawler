# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import sqlite3
import csv

class TeacherPipeline(object):
    def process_item(self, item, spider):
        self.csvfile=open('../teacher.csv','a',newline='')
        writer=csv.writer(self.csvfile)
        data=[item['grade'], item['subject'],item['gender'],item['other'],item['time'],item['reward']]
        writer.writerow(data)
        return item

    def spider_close(self):
        self.csvfile.close()
