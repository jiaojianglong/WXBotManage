#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/20
# @Author  : JiaoJianglong

import logging
from redis import ConnectionPool, Redis
from tools.utils import Singleton
from settings import REDIS_DB



class RedisTool(metaclass=Singleton):
    def __init__(self):
        self._connection_pool = ConnectionPool(max_connections=REDIS_DB['MAX_CONNECTION'],
                                                host=REDIS_DB['HOST'],
                                                port=REDIS_DB['PORT'],
                                                db=REDIS_DB['DB'],
                                                password=REDIS_DB['PASSWORD'] )

        self._redis = self.get_redis()

    ##############
    ### 字典数据操作
    ##############

    def set(self,key,value, **kwargs):
        self._redis.set(key,value, **kwargs)

    def get(self,key):
        value = self._redis.get(key)
        return value

    # 保存一条记录，默认添加到最前面
    def save_key_value(self, key, value, append=False):
        if append:
            self._redis.rpush(key, value)
        else:
            self._redis.lpush(key, value)

    # 保存多条记录，默认添加到最前面
    def save_key_values(self, key, value_list, append=False):
        if not isinstance(value_list, list) and not isinstance(value_list, tuple):
            return
        if len(value_list) <= 0:
            return
        if append:
            self._redis.rpush(key, *value_list)
        else:
            self._redis.lpush(key, *value_list)

    # 获取一条记录
    def get_key_value(self, key, index):
        value = self._redis.lindex(key, index)
        return value

    # 获取多条记录
    def get_key_values(self, key, start=0, end=-1):
        values = self._redis.lrange(key, start, end)
        return values

    # 获取键对应记录集的长度
    def get_key_values_length(self, key):
        length = self._redis.llen(key)
        return length

    # 删除一条记录
    def delete_key_value(self, key, value):
        self._redis.lrem(key, value)

    # 删除多条记录
    def delete_key_values(self, key, value_list):
        for value in value_list:
            self._redis.lrem(key, value)

    # 删除一个key
    def delet_key(self, key):
        self._redis.delete(key)

    # key是否存在
    def has_key(self, key):
        return self._redis.exists(key)

    # 创建一个key,并添加值(如果key存在，则先删除再创建)
    def create_key_values(self, key, value_list, append=False):
        if self.has_key(key):
            self.delet_key(key)
        self.save_key_values(key, value_list, append)

    # 获得一个redis实例
    def get_redis(self):
        return Redis(connection_pool=self._connection_pool)

    #创建一个key-value
    def set_redis_key_value(self, key, value):
        self._redis.set(key,value)

    # 获取keys
    def get_keys(self, pattern):
        cache_keys = self._redis.keys(pattern)
        keys = [key.decode("utf-8") for key in cache_keys]
        return keys

    ##############
    ### 集合数据操作
    ##############

    # 向集合中添加一个或多个成员
    def sadd(self, key, members):
        self._redis.sadd(key, members)

    # 获取集合的成员数
    def scard(self, key):
        return self._redis.scard(key)

    # 判断 member 元素是否是集合 key 的成员
    def sismember(self, key, member):
        return self._redis.sismember(key, member)

    # 返回集合中的所有成员
    def smembers(self, key):
        return self._redis.smembers(key)

    # 将 member 元素从 source 集合移动到 destination 集合
    def smove(self, source, destination, member):
        self._redis.smove(source, destination, member)

    # 返回集合中一个或多个随机数
    def srandmember(self, key, count=1):
        return self._redis.srandmember(key, count)

    # 移除集合中一个或多个成员
    def srem(self, key, members):
        self._redis.srem(key, members)

redis_client = RedisTool()
info = "初始化redis客户端:%s"%redis_client._redis
logging.warning("\033[1;32;40m" + str(info) + "\033[0m")

if __name__ == "__main__":
    redis_tool = RedisTool()
    print(redis_tool.get_keys("law_*")[0:10])