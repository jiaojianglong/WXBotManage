#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 0014 20:17
# @Author  : jiaojianglong
import re
from weixin_bot.client.msg import Msg
from weixin_bot.tuling.tuling_replay import tuling_replay


class EmoticonMassage(Msg):
    type_ = "emoticon"

    def handle(self):
        # TODO 表情需要自己处理，建立库，搜集新的表情，人工绑定回答的表情，可斗图
        re_cdnurl = re.search(r'cdnurl(| )=(| )"(?P<cdnurl>.*?)"', self.text)
        emoticon_url = re_cdnurl.group("cdnurl")
        self.sendImage("emoticon.gif", emoticon_url)

        tuling_replay(dict(msg_type=1,
                           imageUrl=emoticon_url,
                           user_id=self.msg.user_id,
                           group_id=self.msg.group_id, ), self)

        print("收到表情：", emoticon_url)
