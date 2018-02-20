# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re,datetime

import scrapy
from scrapy.loader.processors import MapCompose
from settings import MYSQL_DATE_FORMAT,MYSQL_DATETIME_FORMAT
# from utils.common import extract_num


class ZhihuQuestionItem(scrapy.Item):
    # 知乎问题的 item
    question_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    watch_user_nums = scrapy.Field()
    click_nums = scrapy.Field()
    create_time = scrapy.Field()

    @staticmethod
    def extract_num(string):
        match_obj = re.match(r'.*(\d+).*',string)
        if match_obj:
            return int(match_obj.group(1))
        else:
            return 0

    def get_sql_param(self):
        sql = '''
            INSERT INTO zhihu_question(crawl_time,question_id,topics,url,title,content,answer_nums,comment_nums,watch_user_nums)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE content=VALUES(content),answer_nums=VALUES(answer_nums),comment_nums=VALUES(comment_nums),watch_user_nums=VALUES(watch_user_nums)
        '''
        question_id = ''.join(self['question_id'])
        topics = ';'.join(self['topics'])
        url = ''.join(self['url'])
        title = ''.join(self['title'])
        content = ''.join(self['content'])
        answer_nums = self.extract_num(self['answer_nums'][0])
        comment_nums = self.extract_num(self['comment_nums'][0])
        watch_user_nums = self.extract_num(self['watch_user_nums'][0])
        create_time = datetime.datetime.now().strftime(MYSQL_DATETIME_FORMAT)
        param = (create_time,question_id,topics,url,title,content,answer_nums,comment_nums,watch_user_nums)
        return sql,param


class ZhihuAnswerItem(scrapy.Item):
    # 知乎问题的 item
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    comment_nums = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_sql_param(self):
        sql = '''
                    INSERT INTO zhihu_answer(zhihu_id,question_id,author_id,content,crawl_time,create_time,update_time,url)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE content=VALUES(content),create_time=VALUES(create_time),update_time=VALUES(update_time)

                '''
        zhihu_id = self['zhihu_id']
        question_id = self['question_id']
        author_id = self['author_id']
        content = self['content']
        crawl_time = self['crawl_time'].strftime(MYSQL_DATE_FORMAT)
        create_time = datetime.datetime.fromtimestamp(self['create_time']).strftime(MYSQL_DATETIME_FORMAT)
        update_time = datetime.datetime.fromtimestamp(self['update_time']).strftime(MYSQL_DATETIME_FORMAT)
        url = self['url']
        param = (zhihu_id,question_id,author_id,content,crawl_time,create_time,update_time,url)
        return sql,param
