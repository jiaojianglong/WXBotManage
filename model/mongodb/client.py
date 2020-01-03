#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/18
# @Author  : JiaoJianglong


from model.connect.mongodb import MongoDB
from bson.objectid import ObjectId


class Client(MongoDB):
    _fields = ["name", "host", "send_port", "accept_port"]
    name = "x_qa.client"

    def get_all_clients(self):
        res = self.search_read(pager_flag=False)[0]
        clients = [{"name": client.get("name"),
                    "host": client.get("host"),
                    "accept_port": int(client.get("accept_port")),
                    "send_port": int(client.get("send_port")),
                    "_id": client.get("_id")} for client in res]
        return clients

    def get_client_name_by_id(self, client_id):
        return self.find_one(query_params={"_id": ObjectId(client_id)}).get(
            "name", "")
