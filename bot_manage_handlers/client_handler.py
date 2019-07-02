#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/3/18
# @Author  : JiaoJianglong

import time

from bot_manage_handlers.base.basehandler import BaseHandler
from model.mongodb.client import Client
from bson.objectid import ObjectId
from weixin_bot.connect_bot.tcp_client import TCPClient

class ClientHandler(BaseHandler):
    client_model = Client()

    @BaseHandler.decorator.threadpool_decorator
    def get(self, *args, **kwargs):
        try:
            name = self.get_argument("name","")
            page = int(self.get_argument("page",1))
            page_size = int(self.get_argument("page_size",10))
            is_all = self.get_argument("is_all","")
        except:
            raise self.exception.CustomException("参数格式错误")

        result = self.init_parameter()
        collection_client_info = {tcp_client.id:{"connect_state":tcp_client.connect_state,"wxbot":tcp_client.client.get_weixin_num(),"name":tcp_client.name} for tcp_client in TCPClient.connect_list}

        if is_all:
            client_info = [{"client_id":client_id,"name":client.get("name")}for client_id,client in collection_client_info.items()]
            result['data'] = client_info
            return result
        query_params = {}
        if name:
            query_params.update({"name":name})
        all_client_info,page = self.client_model.search_read(page=page,page_size=page_size,query_params=query_params)
        for client in all_client_info:
            if client.get("_id") in collection_client_info.keys():
                client['connect_state'] = collection_client_info[client.get("_id")].get("connect_state")
                client['wxbot'] = collection_client_info[client.get("_id")].get("wxbot")
            else:
                client['connect_state'] = False
                client['wxbot'] = []

        result['data'] = all_client_info

        return result


    @BaseHandler.decorator.threadpool_decorator
    def post(self):
        result = self.init_parameter()
        try:
            name = self.get_argument("name")
            host = self.get_argument("host")
            accept_port = self.get_argument("accept_port")
            send_port = self.get_argument("send_port")
            client_id = self.get_argument("_id","")
        except:
            raise self.exception.CustomException("参数格式错误")
        if client_id: #更新操作
            self.client_model.update({"name":name,"host":host,"accept_port":accept_port,"send_port":send_port},
                                     query_params={"_id":ObjectId(client_id)})
        else:
            self.client_model.create({"name":name,"host":host,"accept_port":accept_port,"send_port":send_port})
        result['data'] = "success"
        return result


    @BaseHandler.decorator.threadpool_decorator
    def delete(self, *args, **kwargs):
        result = self.init_parameter()
        client_id = self.get_argument("client_id")
        self.client_model.delete(query_params = {"_id":ObjectId(client_id)})
        result['data'] = "success"
        return result



class ConnectClientHandler(BaseHandler):
    client_model = Client()
    @BaseHandler.decorator.threadpool_decorator
    def post(self, *args, **kwargs):
        result = self.init_parameter()
        client_id = self.get_argument("client_id")
        connect_state = self.get_argument("connect_state")
        if connect_state == "true": #创建连接
            client_info = self.client_model.find_one(query_params={"_id":ObjectId(client_id)})
            client = TCPClient(client_info).connect()
            while client.connecting:
                time.sleep(0.1)
            result['data'] = client.connect_state
        else:  #断开连接
            for client in TCPClient.connect_list:
                if client.id == client_id:
                    client.close()
                    result['data'] = client.connect_state
        return result



class ClientLoginHandler(BaseHandler):

    @BaseHandler.decorator.threadpool_decorator
    def get(self, *args, **kwargs):
        result = self.init_parameter()
        client_id = self.get_argument("client_id")
        for client in TCPClient.connect_list:
            if client.id == client_id:
                file_name = client.client.get_QR_code()
        result['data']['login_image'] = "/static/"+file_name
        return result


    @BaseHandler.decorator.threadpool_decorator
    def post(self, *args, **kwargs):
        result = self.init_parameter()
        client_id = self.get_argument("client_id")

        for client in TCPClient.connect_list:
            if client.id == client_id:
                client.client.start_up()
        result['data'] = "success"
        return result


class AutoFriendHandler(BaseHandler):

    client_model = Client()
    @BaseHandler.decorator.threadpool_decorator
    def get(self, *args, **kwargs):
        result = self.init_parameter()
        client_id = self.get_argument("client_id")
        status_flag = True if self.get_argument("auto_friend_state","") == "true" else False

        self.client_model.update({"auto_friend":status_flag},query_params={"_id":ObjectId(client_id)})

        for client in TCPClient.connect_list:
            if client.id == client_id:
                wx_status = client.client.auto_friend()
                if wx_status != status_flag:
                    client.client.auto_friend()

        result['data'] = "success"
        return result

class AutoGroupHandler(BaseHandler):

    client_model = Client()
    @BaseHandler.decorator.threadpool_decorator
    def get(self, *args, **kwargs):
        result = self.init_parameter()
        client_id = self.get_argument("client_id")
        status_flag = True if self.get_argument("auto_group_state","") == "true" else False

        self.client_model.update({"auto_group":status_flag},query_params={"_id":ObjectId(client_id)})

        for client in TCPClient.connect_list:
            if client.id == client_id:
                wx_status = client.client.auto_group()
                if wx_status != status_flag:
                    client.client.auto_group()

        result['data'] = "success"
        return result
