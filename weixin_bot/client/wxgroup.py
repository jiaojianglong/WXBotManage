#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/15 0015 19:12
# @Author  : jiaojianglong

from weixin_bot.client.wxmember import WXMember

class WXGroup():

    def __init__(self,wxbot,group_id):
        self.wxbot = wxbot
        self.group_id = group_id


    def get_members(self):
        res = self.wxbot.client.sendmassage.sendmsg_getreturn("2|%s|%s" % (self.wxbot.bot_id, self.group_id))
        if res == "error":
            return []
        res = res.replace("QYLB‘", "")
        members_str_list = res.split("—")
        members = []
        for members_str in members_str_list:
            if members_str:
                try:
                    member_list = members_str.split("‘")
                    member_dict = {}
                    member_dict['member_name'] = member_list[1]
                    member_dict['member_wxid'] = member_list[2]
                    members.append(member_dict)
                except:
                    pass
        return members

    def get_members_by_name(self,name):
        members = self.get_members()
        for member in members:
            if member.get("member_name") == name:
                member_wxid = member.get("member_wxid")
                break
        else:
            raise Exception("not exists")
        return member_wxid

    def member(self,member_id):
        return WXMember(self,member_id)