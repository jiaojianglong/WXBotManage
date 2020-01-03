#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/19
# @Author  : JiaoJianglong

import json
from bot_manage_handlers.base.basehandler import BaseHandler
from weixin_bot.connect_bot.tcp_client import TCPClient
from model.mongodb.wxbot import WXbot
from model.mongodb.friend import FriendModel
from model.mongodb.client import Client


class BotHandler(BaseHandler):
    bot_model = WXbot()
    friend_model = FriendModel()
    client_model = Client()

    @BaseHandler.decorator.threadpool_decorator
    def get(self, *args, **kwargs):
        result = self.init_parameter()
        try:
            nickname = self.get_argument("nickname", "")
            client_id = self.get_argument("client_id", "")
            page = int(self.get_argument("page", 1))
            page_size = int(self.get_argument("page_size", 10))
        except Exception:
            raise self.exception.CustomException("参数格式错误")

        login_wx_list = {bot.get("weixin_wxid"): {
            "bot_info": bot,
            "client_id": client.id,
            "client_name": client.name}
                        for client in TCPClient.connect_list
                        for bot in client.client.get_weixin_num()}
        query_params = {}
        if nickname:
            query_params.update({"nickname": nickname})
        if client_id:
            query_params.update({"last_login_client": client_id})

        all_wx_list = self.bot_model.search_read(page=page,
                                                 page_size=page_size,
                                                 query_params=query_params)
        for wx_info in all_wx_list:
            if wx_info.get("wxid") in login_wx_list.keys():
                wx_info['is_login'] = True
                wx_info['client_name'] = login_wx_list[
                    wx_info.get("wxid")].get("client_name", "")
                wx_info['client_id'] = login_wx_list[wx_info.get("wxid")].get(
                    "client_id", "")
            else:
                wx_info['is_login'] = False
                wx_info['client_name'] = ""
                wx_info['client_id'] = wx_info.get("last_login_client")

            friend_num = self.friend_model.get_count(
                {"bot_wxid": wx_info.get("wxid"), "type": "好友"})
            wx_info['friend_num'] = friend_num
            group_num = self.friend_model.get_count(
                {"bot_wxid": wx_info.get("wxid"), "type": "群聊"})
            wx_info['group_num'] = group_num

        result['data'] = all_wx_list
        return result


class BotDetailHandler(BaseHandler):
    bot_model = WXbot()
    friend_model = FriendModel()

    @BaseHandler.decorator.threadpool_decorator
    def get(self, *args, **kwargs):
        result = self.init_parameter()
        wxid = self.get_argument("wxid")

        res = self.bot_model.find_one(query_params={"wxid": wxid})

        friend, _ = self.friend_model.search_read(
            query_params={"bot_wxid": wxid, "type": "好友"}, pager_flag=False)
        group, _ = self.friend_model.search_read(
            query_params={"bot_wxid": wxid, "type": "群聊"}, pager_flag=False)
        result['data'] = {"base_info": res, "friend": friend, "group": group}
        return result

    @BaseHandler.decorator.threadpool_decorator
    def post(self, *args, **kwargs):
        result = self.init_parameter()
        try:
            # wxid = self.get_argument("wxid")

            body = dict(
                is_add_group_hellow=True if self.get_argument(
                    "is_add_group_hellow", "") == "true" else False,
                add_group_hellow=[words for words in
                                  self.get_argument("add_group_hellow",
                                                    "").split("\n") if words],
                is_welcome_member=True if self.get_argument(
                    "is_welcome_member", "") == "true" else False,
                welcome_member=[words for words in
                                self.get_argument("welcome_member", "").split(
                                    "\n") if words],
                is_add_friend_hellow=True if self.get_argument(
                    "is_add_friend_hellow", "") == "true" else False,
                add_friend_hellow=[words for words in
                                   self.get_argument("add_friend_hellow",
                                                     "").split("\n") if words],
                is_keyword=True if self.get_argument("is_keyword",
                                                     "") == "true" else False,
                keywords=json.loads(self.get_argument("keywords")),
                reply_pattern=int(self.get_argument("reply_pattern"))
            )
            print(body)
            # res = self.bot_model.save(body, count_params={"wxid": wxid})
            result['data'] = "success"
        except Exception:
            result['data'] = "error"
        return result
