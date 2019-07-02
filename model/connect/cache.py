#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/20
# @Author  : JiaoJianglong


from models.connect.redis import redis_client

class Cache(object):
    redis = redis_client

    @classmethod
    def get(cls,key):
        try:
            value = redis_client.get(key)
        except:
            value = b""
        if value:
            try:
                value =  value.decode("utf-8")
            except:
                value = None
        return value

    @classmethod
    def set(cls, key, value):
        redis_client.set(key, value)
