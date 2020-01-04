#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/21
# @Author  : JiaoJianglong


from model.connect.mongodb import MongoDB


class FriendModel(MongoDB):
    name = "wxmanage.friend"

    def save_or_update(self, friend, bot_id, bot_name):
        head_url = "https://timgsa.baidu.com/timg?image&quality=80&size=" \
                   "b9999_10000&sec=1553225913439&di=98fca8aaed1f4c6748fd" \
                   "fdc220a95999&imgtype=0&src=http%3A%2F%2Fhbimg.b0." \
                   "upaiyun.com%2F69ad7a731f43d4b8729f1a2fbe65c43801ca" \
                   "0f033250-EV1vMf_fw658"
        if friend.get("friend_headportrait") == "无":
            friend['friend_headportrait'] = head_url

        super(FriendModel, self).save({"type": friend.get("friend_type"),
                                       "nickname": friend.get("friend_name"),
                                       "wxnum": friend.get("friend_wxnum"),
                                       "wxid": friend.get("friend_wxid"),
                                       "wxv1": friend.get("friend_wxv1"),
                                       "remarkname": friend.get(
                                           "friend_remarkname"),
                                       "headportrait": friend.get(
                                           "friend_headportrait"),
                                       "status": friend.get("friend_status"),
                                       "bot_wxid": bot_id,
                                       "bot_name": bot_name}, count_params={
            "wxid": friend.get("friend_wxid")})
