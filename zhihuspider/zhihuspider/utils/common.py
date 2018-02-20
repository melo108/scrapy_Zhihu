# _*_ coding:utf-8 _*_
__author__ = 'jimmy'
__date__ = '2018/2/20 14:23'

import re

def extract_num(string):
    match_obj = re.match(r'.*(\d+).*', string)
    if match_obj:
        return match_obj.group(1)
    else:
        return 0
