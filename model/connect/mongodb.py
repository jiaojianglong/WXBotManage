#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/29
# @Author  : JiaoJianglong


_author="niyoufa"


import logging
import math
import json

import urllib.parse
import datetime
import pymongo
import pymongo.cursor
import pymongo.command_cursor
import pymongo.results
from bson.objectid import ObjectId
from bson.json_util import dumps
from tornado.options import options

from setting import MONGO_DB
from bot_manage_handlers.base import exceptions


uri = "mongodb://%s:%s@%s" % (
        urllib.parse.quote(MONGO_DB.get("USERNAME")),
        urllib.parse.quote(MONGO_DB.get("PASSWORD")),
        "%s:%s/%s" %
        (MONGO_DB.get("HOST"), MONGO_DB.get("PORT"), MONGO_DB.get("DB")))

mongo_client = pymongo.MongoClient(uri)

info = "初始化mongodb客户端:%s"%str(mongo_client)
logging.warning("\033[1;32;40m" + str(info) + "\033[0m")

class MongoDB():
    exceptionlib = exceptions
    name = ""
    def __init__(self):
        self.coll = self.get_coll()

    def coll_name(self):
        return self.name.split(".")[1]

    def db_name(self):
        return self.name.split(".")[0]

    def get_coll(self):
        db_name = self.name.split(".")[0]
        coll_name = self.name.split(".")[1]
        db = mongo_client[db_name]
        coll = db[coll_name]
        return coll

    def check_columns(self, columns, vals):
        if not isinstance(columns, list):
            raise Exception("columns参数类型错误")
        if not isinstance(vals, dict):
            raise Exception("vals 参数类型错误！")
        for column in columns:
            if not column in vals or not vals.get(column):
                raise Exception("字段%s不能为空！"%column)

    def get_count(self,query_params):
        query_params.update(
            is_enable=True,
        )
        count = self.coll.find(query_params).count()
        return count

    def save(self, vals, count_params=None, upsert=True):
        if count_params and self.get_count(count_params):
            obj = self.coll.find_one(count_params)
            obj.update(vals)
            self.coll.save(obj)
        else:
            if upsert:
                obj = vals
                self.create(vals)
            else:
                obj = {}
        return self.dump(obj)

    def create(self,vals,*args,**kwargs):
        curr_time = str(datetime.datetime.now())
        vals["create_date"] = curr_time
        vals["write_date"] = curr_time
        vals["is_enable"] = True

        vals["maintain"] = [dict(
            operation_time = curr_time,
            user_name ="未知",
            operation_type = "create",
        )]
        self.coll.insert_one(vals)
        return self.dump(vals)

    def find_one(self, *args, **kwargs):
        # 检查查询参数
        if not "query_params" in kwargs:
            raise Exception("查询参数query_params不存在！")
        if not isinstance(kwargs.get("query_params"), dict):
            raise Exception("查询参数query_params:%s, 类型错误！"%kwargs.get("query_params"))
        if not kwargs.get("query_params"):
            raise Exception("查询参数query_params:%s, 不能为空！"%kwargs.get("query_params"))

        # 查询参数
        query_params = kwargs.get("query_params")
        query_params.update(dict(
            is_enable=True,
        ))
        obj = self.coll.find_one(query_params)
        if not obj:
            raise Exception("不存在:%s！"%query_params)
        return self.dump(obj)

    def search(self,page=1,page_size=10,*args,**kwargs):
        # 查询参数
        query_params = kwargs.get("query_params") or {}
        query_params.update(dict(
            is_enable=True,
        ))

        # 排序参数
        sort_params = kwargs.get("sort_params") or {}
        if sort_params == {}:
            sort_params.update({"create_date": -1})

        if kwargs.get("pager_flag") != False:
            pager_flag = True  # 是否分页
        else:
            pager_flag = False

        if pager_flag:
            length = self.coll.find(query_params).count()
            pager = self.count_page(length, page, page_size)
            cr = self.coll.aggregate([
                {"$match": query_params},
                {"$sort": sort_params},
                {"$skip": pager['skip']},
                {"$limit": pager['page_size']}])
        else:
            pager = self.count_page(0, 0, 0)
            cr = self.coll.aggregate([
                {"$match": query_params},
                {"$sort": sort_params}])

        ids = []
        for obj in cr:
            obj = self.dump(obj)
            ids.append(obj.get("_id"))

        return ids, pager

    def read(self,ids,fields=None,*args,**kwargs):
        query_params = {}
        query_params.update(dict(
            is_enable=True,
        ))

        objectids = []
        for _id in ids:
            id = self.create_objectid(_id)
            objectids.append(id)
        query_params.update({
            "_id":{"$in":objectids}
        })

        cr = self.coll.aggregate([
            {"$match": query_params}])
        objs = []
        for obj in cr:
            obj = self.dump(obj)
            objs.append(obj)
        return objs

    def search_read(self,page=1,page_size=10,*args,**kwargs):
        # 查询参数
        query_params = kwargs.get("query_params") or {}
        query_params.update(dict(
            is_enable=True,
        ))

        # 排序参数
        sort_params = kwargs.get("sort_params")

        if kwargs.get("pager_flag") != False:
            pager_flag = True  # 是否分页
        else:
            pager_flag = False

        _project = kwargs.get("_project") or {}
        if isinstance(_project, str):
            try:
                _project = json.loads(_project)
            except:
                raise Exception("_project参数格式错误！")
        if not isinstance(_project, dict):
            raise Exception("_project参数格式错误！")

        objs = []
        pager = self.count_page(0, page, page_size)
        try:
            aggregate_obj = [
                    {"$match": query_params},
            ]

            if sort_params:
                aggregate_obj.append({"$sort": sort_params})

            if pager_flag:
                length = self.coll.find(query_params).count()
                pager = self.count_page(length, page, page_size)
                aggregate_obj.extend([
                    {"$skip": pager['skip']},
                    {"$limit": pager['page_size']}
                ])

            if _project:
                aggregate_obj.extend([
                    {"$project":_project},
                ])

            cr = self.aggregate(aggregate_obj)

            for obj in cr:
                obj = self.dump(obj)
                objs.append(obj)

        except:
            raise

        for obj in objs:
            maintain = obj.get("maintain")
            if maintain:
                obj["maintain"] = obj["maintain"][:1] + obj["maintain"][-1:]

        return objs, pager

    def write(self,vals,ids=[],*args,**kwargs):
        query_params = {}
        query_params.update(dict(
            is_enable=True,
        ))

        objectids = []
        for _id in ids:
            id = self.create_objectid(_id)
            objectids.append(id)
        query_params.update({
            "_id": {"$in": objectids}
        })

        cr = self.coll.find(query_params)
        curr_date = str(datetime.datetime.now())
        vals.update(dict(
            write_date = curr_date,
        ))
        for obj in cr:
            obj.update(vals)
            obj["maintain"] = obj.get("maintain") or []
            obj["maintain"].append(dict(
                operation_time=curr_date,
                user_name="未知",
                operation_type="update",
            ))
            obj["maintain"] = obj["maintain"][0:] + obj["maintain"][:-1]
            self.coll.save(obj)

    def update(self,vals,*args,**kwargs):
        query_params = kwargs.get("query_params") or {}
        if not query_params:
            raise self.exceptionlib.CustomException("查询参数不能为空！")

        count = self.get_count(query_params)
        if count != 1:
            raise Exception("需要更新的数据个数：%s, 查询条件错误：%s！"%(count, query_params))

        query_params.update(dict(
            is_enable=True,
        ))
        cr = self.coll.find(query_params)
        curr_date = str(datetime.datetime.now())

        if not vals:
            raise self.exceptionlib.CustomException("更新内容不能为空！")

        vals.update(dict(
            write_date=curr_date,
        ))
        for obj in cr:
            obj.update(vals)
            obj["maintain"] = obj.get("maintain") or []
            obj["maintain"].append(dict(
                operation_time=curr_date,
                user_name="未知",
                operation_type="update",
            ))
            obj["maintain"] = obj["maintain"][:1] + obj["maintain"][-1:]
            self.coll.save(obj)
        return self.dump(self.coll.find_one(query_params))

    def update_multi(self, *args, **kwargs):
        filter = kwargs.get("query_params")
        update = kwargs.get("update_params")
        if not filter:
            raise self.exceptionlib.CustomException("查询参数不能为空！")
        elif not isinstance(filter, dict):
            raise self.exceptionlib.CustomException("查询参数类型错误，必须是dict类型！")
        else:
            filter.update(dict(
                is_enable = True,
            ))
        if not update:
            raise self.exceptionlib.CustomException("更新参数不能为空！")
        elif not isinstance(update, dict):
            raise self.exceptionlib.CustomException("更新参数类型错误，必须是dict类型！")
        else:
            if "$set" in update and isinstance(update["$set"], dict):
                update["$set"].update(dict(
                    write_date = str(datetime.datetime.now())
                ))
        update_result_obj = self.coll.update_many(filter, update=update)
        update_result = dict(
            acknowledged = update_result_obj.acknowledged,
            matched_count = update_result_obj.matched_count,
            modified_count = update_result_obj.modified_count,
        )
        return update_result

    def insert_many(self, docs, *args, **kwargs):
        curr_time = str(datetime.datetime.now())
        username = "未知"
        for vals in docs:
            vals["create_date"] = curr_time
            vals["write_date"] = curr_time
            vals["is_enable"] = True

            vals["maintain"] = [dict(
                operation_time=curr_time,
                user_name=username,
                operation_type="insert_many",
            )]
        if not docs:
            raise self.exceptionlib.CustomException("docs 不能为空！")
        self.coll.insert(docs)

    def unlink(self,ids,*args,**kwargs):
        query_params = kwargs.get("query_params") or {}
        query_params.update(dict(
            is_enable=True,
        ))

        objectids = []
        for _id in ids:
            id = self.create_objectid(_id)
            objectids.append(id)

        query_params.update({
            "_id":{"$in":objectids}
        })

        cr = self.coll.find(query_params)
        curr_date = str(datetime.datetime.now())
        for obj in cr:
            obj.update({"write_date":curr_date,"is_enable":False})
            self.coll.save(obj)

    def delete(self, *args, **kwargs):
        query_params = kwargs.get("query_params") or {}
        query_params.update(dict(
            is_enable=True,
        ))
        cr = self.coll.find(query_params)
        print(cr)
        if not cr:
            raise exceptions.CustomException("不存在%s"%query_params)
        curr_date = str(datetime.datetime.now())
        for obj in cr:
            obj.update({"write_date": curr_date, "is_enable": False})
            self.coll.save(obj)

    def search_unlink(self,*args, **kwargs):
        query_params = kwargs.get("query_params") or {}
        query_params.update(dict(
            is_enable=True,
        ))
        cr = self.coll.find(query_params)
        curr_date = datetime.datetime.now()
        for obj in cr:
            obj.update({"write_date": curr_date, "is_enable": False})
            self.coll.save(obj)

    # 打印
    def dump(self, obj):
        result = None
        if isinstance(obj, pymongo.cursor.Cursor) or \
                isinstance(obj, list) or \
                isinstance(obj, pymongo.command_cursor.CommandCursor):
            result = []
            for _s in obj:
                if type(_s) == type({}):
                    s = {}
                    for (k, v) in _s.items():
                        if type(v) == type(ObjectId()):
                            s[k] = json.loads(dumps(v))['$oid']
                        elif type(v) == type(datetime.datetime.utcnow()):
                            s[k] = v.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                        else:
                            s[k] = v
                else:
                    s = _s
                result.append(s)
        elif isinstance(obj, dict):
            for (k, v) in obj.items():
                if type(v) == type(ObjectId()):
                    obj[k] = json.loads(dumps(v))['$oid']
                elif type(v) == type(datetime.datetime.utcnow()):
                    obj[k] = v.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            result = obj
        elif isinstance(obj, pymongo.results.InsertOneResult):
            result = {"inserted_id": str(obj.inserted_id)}
        elif obj is None:
            result = None
        elif len(obj) == 0:
            result = obj
        return result

        # 生成objectid

    def create_objectid(self, str=None):
        try:
            object_id = ObjectId(str)
        except:
            object_id = ''
        return object_id

    # 计算分页信息
    def count_page(self, length, page, page_size=15, page_show=10):
        page = int(page)
        page_size = int(page_size)
        length = int(length)
        if length == 0:
            return {"enable": False,
                    "page_size": page_size,
                    "skip": 0}
        max_page = int(math.ceil(float(length) / page_size))
        page_num = int(math.ceil(float(page) / page_show))
        pages = list(range(1, max_page + 1)[((page_num - 1) * page_show):(page_num * page_show)])
        skip = (page - 1) * page_size
        if page >= max_page:
            has_more = False
        else:
            has_more = True
        pager = {
            "page_size": page_size,
            "max_page": max_page,
            "pages": pages,
            "page_num": page_num,
            "skip": skip,
            "page": page,
            "enable": True,
            "has_more": has_more,
            "total": length,
        }
        return pager

    def aggregate(self, body):
        cr = self.coll.aggregate(body, allowDiskUse=True)
        return cr