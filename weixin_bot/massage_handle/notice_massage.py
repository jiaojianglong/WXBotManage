#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 0014 20:17
# @Author  : jiaojianglong

import re
from weixin_bot.client.msg import Msg


class NoticeMassage(Msg):
    type_ = "notice"

    def handle(self):
        moved_out_group_regrex = r"你被\".*\"移出群聊"
        if re.match(moved_out_group_regrex, self.text):
            print("机器人被移出群聊")

        in_group_regrex = r"\".*\"邀请你加入了群聊，群聊参与人还有：.*"
        if re.match(in_group_regrex, self.text):
            if self.bot_info.get("is_add_group_hellow"):
                self.reply_text(self.bot_info.get("add_group_hellow")[0] if
                                self.bot_info.get("add_group_hellow")
                                else
                                "大家好，我是%s,初来乍到，请多多关照 "
                                "@我可以和我聊天呦～" % self.bot_info.get(
                    "nickname"))

        other_add_in_group_regrex = r"\".*\"邀请\".*\"加入了群聊"
        if re.match(other_add_in_group_regrex, self.text):
            if self.bot_info.get("is_welcome_member"):
                member_name = re.search(r"邀请\"(?P<name>.*)\"加入了群聊",
                                        self.text).group("name")
                member_wxid = self.wxgroup.get_members_by_name(member_name)
                welcome_member = self.bot_info.get("welcome_member")[
                    0] if self.bot_info.get("welcome_member") else "欢迎欢迎"
                self.reply_at_text("@%s\n" % (member_name) + welcome_member,
                                   member_wxid)

        add_friend_regrex = r"你已添加了.*，现在可以开始聊天了。"
        if re.match(add_friend_regrex, self.text):
            if self.bot_info.get("is_add_friend_hellow"):
                self.reply_text(self.bot_info.get("add_friend_hellow")[
                                    0] if self.bot_info.get(
                    "add_friend_hellow")
                                else "你好啊")
        print("通知消息:", self.text)
