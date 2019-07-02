#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/20
# @Author  : JiaoJianglong


import pymysql
import logging
from settings import MYSQL_DB
from tools.utils import Singleton

class MySQL():
    """
    mysql操作基类，每个数据库创建一个连接,缓存在类中
    """
    connect_dict = {}
        
    def __init__(self,db_name):
        if db_name in self.connect_dict.keys():
            self.connect = self.connect_dict[db_name]
        else:
            self.connect = pymysql.connect(host=MYSQL_DB["HOST"],port=MYSQL_DB["PORT"],user=MYSQL_DB["USER"],password=MYSQL_DB['PASSWORD'],database=db_name)
            self.connect_dict.update({db_name:self.connect})
            info = "初始化mysql客户端:%s" % str(self.connect)
            logging.warning("\033[1;32;40m" + str(info) + "\033[0m")

    def __enter__(self):
        self.cursor = self.connect.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()


