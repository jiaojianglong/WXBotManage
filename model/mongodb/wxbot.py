#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/19
# @Author  : JiaoJianglong

from model.connect.mongodb import MongoDB
class WXbot(MongoDB):
    name="x_qa.bot"
    _field = ["nickname","wxid","phone","last_login_client"]


    def search_read(self,page=1,page_size=10,*args,**kwargs):
        res = super(WXbot,self).search_read(page=1,page_size=10,*args,**kwargs)[0]
        result = [{"nickname":wx.get("nickname"),
                   "wxid":wx.get("wxid"),
                   "phone":wx.get("phone"),
                   "last_login_client":wx.get("last_login_client")} for wx in res]
        return result


    def save_or_update_bot(self,bot,client_id):
        super(WXbot,self).save({"nickname": bot.get("weixin_nickname"),
                             "wxid": bot.get("weixin_wxid"),
                             "phone": bot.get("weixin_phone"),
                             "last_login_client": client_id}, count_params={"wxid": bot.get("weixin_wxid")})




