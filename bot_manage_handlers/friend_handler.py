#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/21
# @Author  : JiaoJianglong


from bot_manage_handlers.base.basehandler import BaseHandler
from model.mongodb.friend import FriendModel

class FriendHandler(BaseHandler):
    friend_model = FriendModel()
    @BaseHandler.decorator.threadpool_decorator
    def get(self, *args, **kwargs):
        result = self.init_parameter()
        name = self.get_argument("name","")
        bot_wxid = self.get_argument("bot_wxid","")
        page = int(self.get_argument("page",1))
        page_size = int(self.get_argument("page_size",10))

        query_params = {}
        if name:
            query_params.update({"nickname":name})
        if bot_wxid:
            query_params.update({"bot_wxid":bot_wxid})
        res,page = self.friend_model.search_read(page=page,page_size=page_size,query_params=query_params)
        result['data'] = res
        return result

