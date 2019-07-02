#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/10 21:56
# @Author  : jiaojianglong


import tornado.ioloop
import tornado.web
from urls import handler
import tornado.httpserver
import weixin_bot.massage_handle
from weixin_bot.connect_bot.connect import CONNS
from setting import _root

application = tornado.web.Application(handler, debug=False, static_path=_root+"/static/")

if __name__ == "__main__":
    print("程序启动成功")
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.bind(8877)
    http_server.start()
    tornado.ioloop.IOLoop.current().start()