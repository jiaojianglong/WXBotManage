#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 0014 13:44
# @Author  : jiaojianglong
from weixin_bot.client.wxbot import WXBot
from weixin_bot.client.wxgroup import WXGroup
from weixin_bot.client.wxfrinend import WxFriend
from weixin_bot.client.wxmember import WXMember
from model.mongodb.client import Client
from model.mongodb.wxbot import WXbot
from model.mongodb.friend import FriendModel
from bson.objectid import ObjectId


class Msg():
    type_ = ""
    client_model = Client()
    bot_model = WXbot()
    friend_model = FriendModel()

    def __init__(self, msg):
        self.msg = msg
        self.tcp_client = msg.client
        self.wxclient = msg.client.client
        self.client_info = self.client_model.find_one(
            query_params={"_id": ObjectId(self.tcp_client)})
        if self.type_ == "connect_success":
            return
        self.wxbot = WXBot(self.wxclient, msg.botid)
        try:
            self.bot_info = self.bot_model.find_one(
                query_params={"wxid": msg.accept_wxid})
        except Exception:
            wx_bots = self.wxclient.get_weixin_num()
            for bot in wx_bots:
                if bot.get("weixin_wxid") == self.msg.accept_wxid:
                    self.bot_model.save_or_update_bot(bot, self.tcp_client.id)
            try:
                self.bot_info = self.bot_model.find_one(
                    query_params={"wxid": msg.accept_wxid})
            except Exception:
                print("获取微信号信息失败")

        if self.type_ == "logout":
            return
        self.text = msg.text
        if msg.is_group:
            self.wxgroup = WXGroup(self.wxbot, msg.group_id)
            self.wxmember = WXMember(self.wxgroup, msg.member)
        else:
            self.wxfriend = WxFriend(self.wxbot, msg.from_wxid)
            # try:
            #     self.friend_info = self.friend_model.find_one(
            # query_params={"wxid":msg.from_wxid})
            # except:
            #     wx_friends = self.wxbot.get_friends()
            #     for friend in wx_friends:

    # 处理函数
    def handle(self):
        raise Exception("子类需复写此方法")

    # 回复text类型消息
    def reply_text(self, text):
        print("发送消息", text)
        self.wxclient.sendmassage.sendmsg(
            "3|%s|%s|%s|0" % (self.msg.botid, self.msg.from_wxid, text))

    def reply_at_text(self, text, at_wxid):
        self.wxclient.sendmassage.sendmsg(
            "10|%s|%s|%s|%s|0" % (
                self.msg.botid,
                self.msg.from_wxid,
                at_wxid,
                text)
        )

    def sendImage(self, filename, fileurl):
        self.wxclient.sendmassage.sendmsg(
            "12|%s|%s|1|%s|%s" % (
                self.msg.botid,
                self.msg.from_wxid,
                filename,
                fileurl)
        )

    def sendFile(self, filename, fileurl):
        self.wxclient.sendmassage.sendmsg(
            "12|%s|%s|2|%s|%s" % (
                self.msg.botid,
                self.msg.from_wxid,
                filename,
                fileurl)
        )
