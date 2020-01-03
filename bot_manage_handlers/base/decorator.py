#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/17
# @Author  : JiaoJianglong

import json
import logging
from tornado import gen
from functools import wraps
from tornado.options import options
from setting import _root
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from bot_manage_handlers.base.exceptions import HandlerError


def catch_except(func):
    """
    最外层装饰器，用来捕捉异常，并返回结果
    :param func:
    :return:
    """

    @gen.coroutine
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            res = yield func(self, *args, **kwargs)
            self.write(res)
        except HandlerError as err:
            logging.exception(err)
            self.write({"code": err.status_code, "msg": err.reason})
        except Exception as e:
            logging.exception(e)
            self.write({"code": 500, "msg": e.args})
            # self.write( {"code": 500, "msg": "系统繁忙，请稍后再试"})

    return wrapper


def async_decorator(func):
    """
    装饰RequestHandler子类中的请求方法，被装饰的子类方法必须用异步方法编写，否则会阻塞整个主线程
    逻辑较简单的请求用比较好
    :param func:
    :return:
    """

    @catch_except
    @gen.coroutine
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        res = yield func(self, *args, **kwargs)
        return res

    return wrapper


executor = ThreadPoolExecutor(32)


def threadpool_decorator(func):
    """
    装饰RequestHandler子类中的请求方法，被装饰的子类方法将在线程中运行
    请求稍微复杂一些的应该使用此装饰器装饰
    :param func:
    :return:
    """

    @catch_except
    @gen.coroutine
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self.executor = executor
        self.add_header('Access-Control-Allow-Origin', '*')
        self.add_header('Access-Control-Allow-Methods', '*')
        res = yield run(self, func, *args, **kwargs)
        return res

    return wrapper


@run_on_executor
def run(self, func, *args, **kwargs):
    return func(self, *args, **kwargs)


class preload():
    '''
    预加载装饰器，判断是否加载缓存数据，并将数据缓存到类中,数据不可做赋值操作
    '''

    def __init__(self, func):
        self.__func = func

    def __get__(self, instance, owner, refresh=False):
        if instance is None:
            return self
        else:
            logging.info("预加载：" + self.__func.__name__)
            if options.use_cache and not refresh:  # 是否使用缓存
                logging.info("使用缓存文件:%s" % self.__func.__name__)
                try:
                    with open(_root + "/resource/cache/%s.txt" %
                              self.__func.__name__, "r", encoding="utf8") as f:
                        res = json.loads(f.read())
                except Exception:
                    res = self.__func(instance)
                    with open(_root + "/resource/cache/%s.txt" %
                              self.__func.__name__, "w", encoding="utf8") as f:
                        f.write(json.dumps(res))
            else:
                res = self.__func(instance)
                with open(_root + "/resource/cache/%s.txt" %
                          self.__func.__name__, "w", encoding="utf8") as f:
                    f.write(json.dumps(res))
            instance.__dict__[self.__func.__name__] = res
            if not hasattr(instance, self.__func.__name__ + "_refresh"):
                instance.__dict__[
                    self.__func.__name__ + "_refresh"] = self.__get__
            return res
