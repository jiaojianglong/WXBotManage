#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/9/10 21:56
# @Author  : jiaojianglong

import os

_root = os.path.dirname(__file__)


MYSQL_INFO = "mysql+pymysql://root:123456@localhost:3306/model"

ES_CONN_INFO = {"hosts":["127.0.0.1:9200"],
                # "http_auth":('user', 'secret'),
                "scheme":"https",
                "port":9200,
                "maxsize":40,
                "timeout":240}

MONGO_DB = dict(
    HOST="127.0.0.1",
    PORT=8975,
    DB="admin",
    USERNAME="admin",
    PASSWORD="root",
    )