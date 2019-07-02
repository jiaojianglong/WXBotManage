#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/18
# @Author  : JiaoJianglong

import socket
from tools.trans_byte_to_string import transformCodec
from setting import clients
class SendMessage():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.reconnectNum = 0

    def connect(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.host, self.port))
        except Exception as e:
            print(e.args)
            raise e
        recvData = self.client.recv(4096).decode("gbk")

    def sendmsg_getreturn(self, msg):
        self.connect()
        self.client.sendall(msg.encode("gbk"))
        msg = ""
        while True:
            recvData_bytes = self.client.recv(4096)
            recvData = transformCodec(recvData_bytes)
            if recvData.endswith("完成"):
                msg += recvData[:recvData.find("完成")]
                break
            msg += recvData
        self.client.close()
        return msg

    def sendmsg(self, msg):
        self.connect()
        self.client.sendall(msg.encode("gbk"))
        self.client.close()

def login():
    SendMessage(clients[0]['host'],clients[0]['send_port']).sendmsg("start up")

if __name__ == "__main__":
    login()