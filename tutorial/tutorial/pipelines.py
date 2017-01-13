# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#from twisted.enterprise import adbapi
from scrapy.exceptions import DropItem
import pymysql
import pymysql.cursors
import redis

class TutorialPipeline(object):
    def __init__(self):
        self.connection = pymysql.connect(
            host='127.0.0.1',
            port= 8889,
			db = 'clawer',
			user = 'lzn',
			passwd = '',
            cursorclass=pymysql.cursors.DictCursor,)

    def process_item(self, item, spider):
        sql = "insert into book values(%s, %s, %s)"
        self.connection.cursor().execute(sql, (item["title"][0], item["link"][0], item["desc"][0]))
        self.connection.commit()
        return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.Redis = redis.StrictRedis(host='localhost',port=6379,db=0)

    def process_item(self, item, spider):
        if self.Redis.exists('url:%s' % item['link']):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.Redis.set('url:%s' % item['link'],1)
            return item

class SohuPipeline(object):
    def __init__(self):
        self.connection = pymysql.connect(
            host='127.0.0.1',
            port=8889,
            db='clawer',
            user='lzn',
            passwd='',
			charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,)

    def process_item(self, item, spider):
        if True:
            sql = "insert into news values(%s, %s, %s)"
            content = ""
            link = ""
            for constr in item["content"]:
                content += constr
                self.connection.cursor().execute(sql, (item["title"][0], content,item["link"]))
                self.connection.commit()
            return item

    def close_spider(self,spider):
        self.connection.close()
