#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 0015 19:11
# @Author  : jiaojianglong

import re
import time
from weixin_bot.client.wxbot import WXBot
from setting import _root


class WXClient():
    def __init__(self, host, send_port, accept_port, sendmassage):
        self.host = host
        self.send_port = send_port
        self.accept_port = accept_port
        self.sendmassage = sendmassage

    def start_up(self):
        """
        启动微信客户端
        :return:
        """
        self.sendmassage.sendmsg("start up")

    def get_QR_code(self):
        """
        获取二维码
        :return:
        """
        res = self.sendmassage.sendmsg_getreturn("QR code")
        res = res.strip(b"CODE")
        file_name = "QR_code_%s.jpg" % str(time.time())
        file = open(_root + "/static/" + file_name, "wb")
        file.write(res)
        file.close()
        return file_name

    def auto_friend(self):
        """
        自动同意加好友
        :return:
        """
        res = self.sendmassage.sendmsg_getreturn("Friends")
        status_flag = False
        status = re.search(r"自动通过好友添加验证(?P<status>.*)成功", res).group("status")
        if status == "打开":
            status_flag = True
        return status_flag

    def auto_group(self):
        """
        自动同意进群
        :return:
        """
        res = self.sendmassage.sendmsg_getreturn("group")
        status_flag = False
        status = re.search(r"自动同意进群(?P<status>.*)成功", res).group("status")
        if status == "打开":
            status_flag = True
        return status_flag

    def get_weixin_num(self):
        """
        获取微信号
        :return:
        """
        recData = self.sendmassage.sendmsg_getreturn("WeChat list")
        if recData.startswith("YXLB"):
            rec = recData.replace("YXLB‘", "")
            if len(rec) > 3:
                weixin_num_list = rec.split("—")
                weixin_list = []
                for weixin_num_str in weixin_num_list:
                    if weixin_num_str:
                        try:
                            weixin_dict = {}
                            weixin_message = weixin_num_str.split("‘")
                            weixin_dict['weixin_num'] = weixin_message[0]
                            weixin_dict['weixin_nickname'] = weixin_message[1]
                            weixin_dict['weixin_phone'] = weixin_message[2]
                            weixin_dict['weixin_id'] = weixin_message[3]
                            weixin_dict['weixin_wxid'] = weixin_message[4]
                            weixin_list.append(weixin_dict)
                        except Exception:
                            pass
                return weixin_list
        return []

    def wx_bot(self, bot_id):
        return WXBot(self, bot_id)
