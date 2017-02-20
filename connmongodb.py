import pymongo

connection = pymongo.MongoClient('127.0.0.1', 27017)
tdb = connection.scrapy
post_info = tdb.weibo
post_info.insert({'name':'wan','age':'22'})
print('Done!')