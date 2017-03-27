# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TeacherItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    grade = scrapy.Field()
    subject = scrapy.Field()
    gender = scrapy.Field()
    other = scrapy.Field()
    time = scrapy.Field()
    reward = scrapy.Field()
