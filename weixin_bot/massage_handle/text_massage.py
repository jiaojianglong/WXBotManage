#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 0014 14:31
# @Author  : jiaojianglong

from weixin_bot.client.msg import Msg
import requests
import re


class TextMassage(Msg):
    type_ = "text"

    def handle(self):
        reply_pattern = self.bot_info.get("reply_pattern", 1)

        if reply_pattern == 1:
            print("不回答")

        elif reply_pattern == 2:
            if self.msg.is_group:
                if not re.search(r'@' + self.bot_info.get("nickname", ""),
                                 self.text):
                    return
                else:
                    self.text = re.sub(
                        r'@' + self.bot_info.get("nickname", ""), "",
                        self.text)

            res = requests.post(url="http://192.168.11.24:8887/api/simple_qa",
                                data={"content": self.text}).json()
            if res.get("data", {}).get("answer"):
                self.reply_text(res.get("data", {}).get("answer"))

            print("回复，群@回复")

        elif reply_pattern == 3:

            res = requests.post(url="http://192.168.11.24:8887/api/simple_qa",
                                data={"content": self.text}).json()
            if res.get("data", {}).get("answer"):
                self.reply_text(res.get("data", {}).get("answer"))

                # tuling_replay(dict(msg_type=0,
                #                text=self.text,
                #                user_id=self.msg.user_id,
                #               group_id=self.msg.group_id,),self)
