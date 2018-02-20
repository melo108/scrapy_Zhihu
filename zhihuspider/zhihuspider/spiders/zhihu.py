# -*- coding: utf-8 -*-
import scrapy
import re,datetime
import json
from urllib.parse import urljoin
#  拼接域名 url

from scrapy.loader import ItemLoader
from zhihuspider.items import ZhihuQuestionItem,ZhihuAnswerItem


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']

    headers = {
        'HOST': 'www.zhihu.com',
        'Referer': 'https://www.zhihu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
    }
    cookies_ = {
        "_xsrf": '',
        "z_c0": "2|1:0|10:1519038396|4:z_c0|92:Mi4xa090T0JRQUFBQUFBd0d2ZmhJRXJEU1lBQUFCZ0FsVk52UDEzV3dEQ201UnZya01KMXJiblZUbTZxNFNCQW4xUkN3|141a68a6a52c85ee1a7e7f2558bb4a85ce40ee5c81f202ba5b18cb085b6663ac",
    }
    # api 接口
    start_answer_url = 'https://www.zhihu.com/api/v4/questions/{0}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}'
    # 知乎 question 的 answer 的起始 url


    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com',callback=self.get_xsrf,headers=self.headers)]

    def get_xsrf(self,response):
        response_text = response.text
        xsrf = re.search(r';xsrf&quot;:&quot;(.*?)&quot', response_text,re.DOTALL)
        if xsrf:
            xsrf= xsrf.group(1)
        else:
            xsrf = ''
        self.cookies_['_xsrf'] = xsrf
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers,cookies=self.cookies_, dont_filter=True,callback=self.parse)

    # @staticmethod
    # def filter_url(url):
    #     import re
    #     if re.match('.*zhihu.com/question/\d+(/.*|$)',url):
    #         return True

    def parse(self,response):
        '''
        提取所有  url  === 深度优先的策略
        其中  question/数字 的url
        :param response:
        :return:
        '''
        all_urls = response.css("a::attr(href)").extract()
        all_urls = [urljoin(response.url,url) for url in all_urls]
        all_urls = list(filter(lambda url:True if url.startswith('https') else False,all_urls ))
        # all_urls = list(filter(lambda url: True  if re.match('.*zhihu.com/question/\d+(/.*|$)',url) else False,all_urls))
        for url in all_urls:
            match_obj = re.match('(.*zhihu.com/question/(\d+))(/.*|$)',url)
            if match_obj:
                request_url = match_obj.group(1)
                question_id = match_obj.group(2)
                # print(request_url,question_id)
                yield scrapy.Request(request_url,meta={'question_id':question_id},headers=self.headers,callback=self.parse_question)
            else:
                yield scrapy.Request(url,headers=self.headers,callback=self.parse)

    def parse_question(self,response):
        """
        获取 详细的 item
        :param response:
        :return:
        """
        question_id = response.meta.get('question_id')
        item_loader = ItemLoader(item=ZhihuQuestionItem(),response=response)
        item_loader.add_css('title','.QuestionHeader-title::text')
        item_loader.add_css('content','.QuestionHeader-detail')
        item_loader.add_value('url',response.url)
        item_loader.add_value('question_id',question_id)
        item_loader.add_css('answer_nums','.List-headerText span::text')
        item_loader.add_css('comment_nums','.QuestionHeader-Comment button::text')
        item_loader.add_css('watch_user_nums','.NumberBoard-itemValue::text')
        item_loader.add_css('topics','.QuestionHeader-topics .Popover div::text')

        question_item = item_loader.load_item()
        yield scrapy.Request(self.start_answer_url.format(question_id,20,0),headers=self.headers,callback=self.parse_answer)
        yield question_item

    def parse_answer(self,response):
        answer_json = json.loads(response.text)
        is_end = answer_json['paging']['is_end']
        totals = answer_json['paging']['totals']

        # 提取 answer 的数据 item

        for answer in answer_json['data']:
            answer_item = ZhihuAnswerItem()
            answer_item['zhihu_id'] = answer['id']
            answer_item['url'] = answer['url']
            answer_item['question_id'] = answer['question']['id']
            answer_item['author_id'] = answer['author']['id'] if 'id' in answer['author'] else None
            answer_item['content'] = answer['content'] if 'content' in answer else None
            answer_item['create_time'] = answer['created_time']
            answer_item['update_time'] = answer['updated_time']
            answer_item['crawl_time'] = datetime.datetime.now()
            yield answer_item

        if not is_end:
            next_url = answer_json['paging']['next']
            yield scrapy.Request(next_url,headers=self.headers,callback=self.parse_answer)












