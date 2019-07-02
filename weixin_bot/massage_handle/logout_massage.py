#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/21
# @Author  : JiaoJianglong

from weixin_bot.client.msg import Msg


class LogoutMassage(Msg):
    type_ = "logout"

    def handle(self):
        print("退出登录")
