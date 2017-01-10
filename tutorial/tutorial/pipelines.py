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
                cursorclass=pymysql.cursors.DictCursor,
		)

	def process_item(self, item, spider):
                sql = "insert into book values(%s, %s, %s)"
                self.connection.cursor().execute(sql, (item["title"][0], item["link"][0], item["desc"][0]))
                self.connection.commit()
		return item
