# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
#from twisted.enterprise import adbapi
import pymysql
import pymysql.cursors


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
        self.titles_seen = set()

    def process_item(self, item, spider):
        if item["title"][0] not in self.titles_seen:
            sql = "insert into news values(%s, %s)"
            content = ""
            for constr in item["content"]:
                content += constr
                self.connection.cursor().execute(sql, (item["title"][0], content))
                self.connection.commit()
            self.titles_seen.add(item["title"][0])
            return item
