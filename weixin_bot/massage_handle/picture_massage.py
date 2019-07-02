#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 0014 20:43
# @Author  : jiaojianglong


import re
from weixin_bot.client.msg import Msg


class PictureMassage(Msg):
    type_ = "picture"

    def handle(self):
        #TODO 表情需要自己处理，建立库，搜集新的表情，人工绑定回答的表情，可实现斗图功能
        re_cdnurl = re.search(r'cdnurl="(?P<cdnurl>.*?)"',self.text)
        emoticon_url = re_cdnurl.group("cdnurl")
        print("收到表情：",emoticon_url)