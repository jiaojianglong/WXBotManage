#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/22
# @Author  : JiaoJianglong


from bot_manage_handlers.client_handler import ClientHandler, \
    ConnectClientHandler, \
    ClientLoginHandler, AutoFriendHandler, AutoGroupHandler
from bot_manage_handlers.bot_handler import BotHandler, BotDetailHandler
from bot_manage_handlers.friend_handler import FriendHandler

handler = [
    (r'/wx/client', ClientHandler),
    (r'/wx/client/connect', ConnectClientHandler),
    (r'/wx/client/login', ClientLoginHandler),
    (r'/wx/client/auto_friend', AutoFriendHandler),
    (r'/wx/client/auto_group', AutoGroupHandler),
    (r'/wx/bot', BotHandler),
    (r'/wx/bot/detail', BotDetailHandler),
    (r'/wx/friend', FriendHandler),
]
