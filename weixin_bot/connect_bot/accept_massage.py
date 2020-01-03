#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 0014 13:02
# @Author  : jiaojianglong


from weixin_bot.client.msg import Msg


class AcceptMassage():
    def __init__(self, msg, client):
        self.client = client
        if msg == "欢迎监听微信消息":  # 连接成功
            self.msg_type = "connect_success"
            return

        msg_list = msg.split("‘")
        if "WXTC" in msg_list:
            self.msg_type = "logout"
            self.botid = msg_list[1]
            return
        from_wxid = msg_list[4]
        text = msg_list[6].strip()
        is_group = False
        member = ""
        if from_wxid.endswith("chatroom"):
            try:
                member = text.split(":")[0]
                # a = text.split(":")[1]
                text = text[text.find(":") + 1:].strip()
            except Exception:
                text = text
                member = ""
            is_group = True

        self.botid = msg_list[0]
        self.msgid = msg_list[1]
        self.msg_type = msg_list[2]
        self.timenum = msg_list[3]
        self.from_wxid = msg_list[4]
        self.accept_wxid = msg_list[5]
        self.text = text
        self.is_group = is_group
        self.member = member
        if self.is_group:
            self.user_id = self.member
            self.group_id = self.from_wxid
        else:
            self.user_id = self.from_wxid
            self.group_id = ""

    def get_msg_type(self):
        if self.msg_type == "connect_success":
            return self.msg_type
        elif self.msg_type == "logout":
            return "logout"
        elif self.msg_type == "1":
            return "text"
        elif self.msg_type == "3":
            return "picture"
        elif self.msg_type == "37":  # 加好友申请
            return "addfriend"
        elif self.msg_type == "47":  # 表情
            return "emoticon"
        elif self.msg_type == "43":  # 视屏
            return "vedio"
        elif self.msg_type == "34":  # 语音
            return "voice"
        elif self.msg_type == "42":  # 名片
            return "wecard"
        elif self.msg_type == "48":  # 位置信息
            return "location"
        elif self.msg_type == "49":  # 连接
            return "link"
        elif self.msg_type == "10000":  # 通知消息
            return "notice"
        elif self.msg_type == "10002":  # 新登录微信
            return "new_bot"
        elif self.msg_type == "self_bot":
            return "self_bot"
        else:
            print("没有记录的消息类型", self.msg_type)
            return self.msg_type

    def reply_massage(self):
        massage_type = self.get_msg_type()
        print("消息类型：", massage_type)
        subclasses = Msg.__subclasses__()
        for subclass in subclasses:
            if subclass.type_:
                if subclass.type_ == massage_type:
                    return subclass(self).handle()
            else:
                raise Exception("子类需复写该属性：type_")
