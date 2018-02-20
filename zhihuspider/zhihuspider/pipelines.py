# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class TwistedMysqlPipeline(object):

    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbparam = dict(
            host=settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )

        dbpool = adbapi.ConnectionPool('MySQLdb',**dbparam)
        return cls(dbpool)

    def process_item(self,item,spider):
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_err)


    def handle_err(self,failure):
        print('处理异常',failure)

    def do_insert(self,cursor,item):
        sql,param = item.get_sql_param()
        cursor.execute(sql,param)



