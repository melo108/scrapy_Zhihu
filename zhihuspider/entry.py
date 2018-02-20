# _*_ coding:utf-8 _*_
__author__ = 'jimmy'
__date__ = '2018/2/19 17:26'
import sys
import os
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy','crawl','zhihu','--nolog'])
# execute(['scrapy','crawl','zhihu'])


