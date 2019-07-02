#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/21
# @Author  : JiaoJianglong
from weixin_bot.client.msg import Msg
from model.mongodb.wxbot import WXbot
from model.mongodb.friend import FriendModel

class NewBotMassage(Msg):
    """新微信登录"""
    type_ = "new_bot"

    bot_model = WXbot()
    friend_model = FriendModel()
    def handle(self):
        print("新微信登录adasssdfds")
        bot = self.wxbot.get_bot_message()
        self.bot_model.save_or_update_bot(bot,self.msg.client.id)
        friends = self.wxclient.wx_bot(bot.get("weixin_num")).get_friends()
        for friend in friends:
            self.friend_model.save_or_update(friend, bot.get("weixin_wxid"),bot.get("weixin_nickname"))