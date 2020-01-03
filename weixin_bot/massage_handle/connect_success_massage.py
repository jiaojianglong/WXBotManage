#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 0015 20:56
# @Author  : jiaojianglong

from weixin_bot.client.msg import Msg
from model.mongodb.wxbot import WXbot
from model.mongodb.friend import FriendModel


class ConnectSuccessMassage(Msg):
    type_ = "connect_success"
    bot_model = WXbot()
    friend_model = FriendModel()

    def handle(self):
        login_bot_list = self.wxclient.get_weixin_num()

        for bot in login_bot_list:
            self.bot_model.save_or_update_bot(bot, self.msg.client.id)
            friends = self.wxclient.wx_bot(bot.get("weixin_num")).get_friends()
            for friend in friends:
                self.friend_model.save_or_update(friend,
                                                 bot.get("weixin_wxid"),
                                                 bot.get("weixin_nickname"))
        print("连接成功")
