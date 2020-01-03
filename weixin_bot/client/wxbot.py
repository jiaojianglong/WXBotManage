#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 0015 19:12
# @Author  : jiaojianglong

from weixin_bot.client.wxfrinend import WxFriend
from weixin_bot.client.wxgroup import WXGroup


class WXBot():
    def __init__(self, client, bot_id):
        self.client = client
        self.bot_id = bot_id

    def get_bot_message(self):
        """
        获取微信号信息
        :return:
        """
        bot_list = self.client.get_weixin_num()
        for bot in bot_list:
            if bot["weixin_num"] == self.bot_id:
                return bot
        return None

    def get_friends(self):
        """
        获取好友列表
        :return:
        """
        res = self.client.sendmassage.sendmsg_getreturn("1|%s" % self.bot_id)
        if res == "error":
            return []
        res = res.replace("HYLB‘", "")
        friend_list = res.split("—")
        friends_list = []
        for friend in friend_list:
            if friend:
                try:
                    friend_info = friend.split("‘")
                    friend_dict = {}
                    friend_dict["friend_type"] = friend_info[1]
                    friend_dict["friend_name"] = friend_info[2]
                    friend_dict["friend_wxnum"] = friend_info[3]
                    friend_dict["friend_wxid"] = friend_info[4]
                    friend_dict["friend_wxv1"] = friend_info[5]
                    friend_dict["friend_remarkname"] = friend_info[6]
                    friend_dict["friend_headportrait"] = friend_info[7]
                    friend_dict["friend_status"] = friend_info[8]
                    friends_list.append(friend_dict)
                except Exception:
                    print("有问题的好友：" + friend)
                    pass
        return friends_list

    def get_groups(self):
        """
        获取群列表
        :return:
        """
        friends = self.get_friends()
        groups = []
        for friend in friends:
            if friend["friend_type"] == "群聊":
                groups.append(friend)
        return groups

    def friend(self, friend_id):
        return WxFriend(self, friend_id)

    def group(self, group_id):
        return WXGroup(self, group_id)
