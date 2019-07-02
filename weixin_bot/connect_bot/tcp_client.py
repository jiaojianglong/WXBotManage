#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/26
# @Author  : JiaoJianglong


import time
import datetime
import socket
import threading

import tornado.ioloop
import tornado.iostream

from tools.trans_byte_to_string import transformCodec
from weixin_bot.connect_bot.accept_massage import AcceptMassage
from weixin_bot.connect_bot.send_massage import SendMessage
from weixin_bot.client.wxclient import WXClient
#TCP连接客户端实例
#需每隔100秒发送一条消息，避免连接断开
class TCPClient(object):
    connect_list = []
    def __init__(self, client, io_loop=None):
        self.id = client['_id']
        self.name = client['name']
        self.host = client['host']
        self.accept_port = int(client['accept_port'])
        self.send_port = int(client['send_port'])
        self.client_info = client
        self.connect_state = False   #连接状态
        self.connecting = False
        self.io_loop = io_loop or tornado.ioloop.IOLoop.current()
        self.shutdown = False
        self.stream = None
        self.sock_fd = None
        self.EOF = b"\xcd\xea\xb3\xc9"
        self.re_connect_num = 0
        self.sendmassage = SendMessage(self.host,self.send_port)
        self.client = WXClient(self.host,self.send_port,self.accept_port,self.sendmassage)

    def get_stream(self):
        self.sock_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = tornado.iostream.IOStream(self.sock_fd)
    #创建连接
    def connect(self):
        self.connecting = True
        self.get_stream()
        self.stream.connect((self.host, self.accept_port), self.start)
        self.stream.set_close_callback(self.on_close)
        return self

    def reconnect(self):
        print("连接断开，重新连接")
        self.connecting = True
        self.connect_state = False
        self.re_connect_num += 1
        self.get_stream()
        self.stream.connect((self.host, self.accept_port), self.start)
        self.stream.set_close_callback(self.on_close)


    def start(self):
        if self not in self.connect_list:
            self.connect_list.append(self)
        self.connect_state = True
        self.re_connect_num = 0
        self.connecting = False
        self.accept_message()

    def accept_message(self):
        self.stream.read_until(self.EOF, self.on_receive)

    def on_receive(self, data):
        self.sendmassage.accept_time = time.time()
        t1 = threading.Thread(target=self.data_reply, kwargs={"data": data})
        t1.start()
        self.accept_message()

    def on_close(self):
        if self.re_connect_num == 2:
            print("尝试重新连接失败，断开连接")
            self.close()
            self.connecting = False
        else:
            time.sleep(1)
            self.reconnect()

    def close(self):
        self.connect_state = False
        if self in self.connect_list:
            self.connect_list.remove(self)
        self.io_loop.close_fd(self.sock_fd)
        print("断开连接")
    #接收消息时调用
    def data_reply(self, **kwargs):
        data = kwargs.get("data")
        msg = transformCodec(data)
        msg = msg[:msg.find("完成")]
        print("%s--接收消息：" % datetime.datetime.now(), msg)
        AcceptMassage(msg,self).reply_massage()
