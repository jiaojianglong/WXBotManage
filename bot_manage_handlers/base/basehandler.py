#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/20
# @Author  : JiaoJianglong
from tornado.web import RequestHandler
from bot_manage_handlers.base import decorator
from bot_manage_handlers.base import exceptions


class BaseHandler(RequestHandler):
    """
    基础接口模块
    """
    exception = exceptions
    decorator = decorator

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init_parameter(self):
        """初始化返回参数"""
        result = {'code': 200, 'msg': '返回成功', 'data': {}}
        return result

    def initialize(self, **kwargs):
        """作为URL规范的第三个参数会作为关键词参数传给该方法"""
        pass

    def on_connection_close(self):
        """客户端关闭连接后调用，清理和长连接相关的资源"""
        pass

    def set_default_headers(self):
        """在请求开始时设置请求头部"""
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE')

    @decorator.threadpool_decorator
    def options(self, *args, **kwargs):
        result = self.init_parameter()
        print("接收到options请求")
        return result
