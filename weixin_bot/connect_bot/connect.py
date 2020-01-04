#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 0014 11:49
# @Author  : jiaojianglong
import time
from weixin_bot.connect_bot.tcp_client import TCPClient
from model.mongodb.client import Client

clients = Client().get_all_clients()
for client in clients:
    res = TCPClient(client).connect()

CONNS = TCPClient.connect_list


def send_thread():
    while True:
        for i in range(60):
            for client in CONNS:
                if not client.sendmassage.sending:
                    client.sendmassage.send()
                    client.sendmassage.sending = True
            time.sleep(1)
            if i == 20:
                for client in CONNS:
                    try:
                        client.stream.write(b"lalala")
                        client.re_connect_num = 0
                    except Exception:
                        if client.re_connect_num < 100:
                            client.reconnect()
