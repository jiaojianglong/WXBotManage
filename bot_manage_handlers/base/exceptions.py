#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/17
# @Author  : JiaoJianglong

from tornado.web import HTTPError


class HandlerError(HTTPError):
    """请求响应处理异常类, 继承该异常类的异常会被全局捕捉，详见utils/decorator.py"""


class RequestTimesError(HandlerError):
    """
    请求次数超限制
    """
    def __init__(self):
        super(RequestTimesError, self).__init__(
            4003, "请求次数超限制")
        self.arg_name = "请求次数超限制"
        self.reason = "请求次数超限制"

class IllegalRequestError(HandlerError):
    """
    非法请求
    """
    def __init__(self):
        super(IllegalRequestError, self).__init__(
            4004, "非法请求")
        self.arg_name = "非法请求"
        self.reason = "非法请求"

class RequestEncryptError(HandlerError):
    """
    请求加密错误
    """
    def __init__(self):
        super(RequestEncryptError, self).__init__(
            4005, "请求加密错误")
        self.arg_name = "请求加密错误"
        self.reason = "请求加密错误"
        
class MissingArgumentError(HandlerError):
    """缺失请求参数错误"""

    def __init__(self, arg_name):
        super(MissingArgumentError, self).__init__(
            4006, '缺失请求参数 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '缺失请求参数 %s' % arg_name


class ArgumentTypeError(HandlerError):
    """参数类型错误"""

    def __init__(self, arg_name):
        super(ArgumentTypeError, self).__init__(
            400, '%s' % arg_name)
        self.arg_name = arg_name
        self.reason = '%s' % arg_name




class EnumError(HandlerError):
    """枚举异常"""

    def __init__(self, arg_name):
        super(EnumError, self).__init__(
            400, '枚举参数错误 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '枚举参数错误 %s' % arg_name

class AuthError(HandlerError):
    """认证错误"""

    def __init__(self, arg_name):
        super(HandlerError, self).__init__(
            401, '认证错误 %s' % arg_name)
        self.arg_name = arg_name
        self.reason = '认证错误 %s' % arg_name
        
class CustomException(HandlerError):
    """
    用户传参错误
    """

    def __init__(self,error_info):
        super(HandlerError,self).__init__(4002,error_info)
        self.arg_name = error_info
        self.reason = error_info
