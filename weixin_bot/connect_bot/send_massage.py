#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 0014 15:22
# @Author  : jiaojianglong




import time
import datetime
import tornado.ioloop
import tornado.iostream
from tornado import gen, queues
from tornado.tcpclient import TCPClient
from tools.trans_byte_to_string import transformCodec, transtoCode

class SendMessage():
    def __init__(self, host, port, io_loop=None):
        self.host = host
        self.port = port
        self.accept_time = time.time()
        self.MSG_LIST = queues.Queue()
        self.RETURN_MSG_LIST = []
        self.sending = False
        if io_loop:
            self.io_loop = io_loop
        else:
            self.io_loop = tornado.ioloop.IOLoop.current()
        self.lastsend_time = time.time()
        self.lastsend_msg = ""

    def change_last_time(self):
        if self.accept_time-self.lastsend_time < 0.05:
            print("时间小于0.05，重新发送***********************************************")
            self.MSG_LIST.put(self.lastsend_msg)

    @gen.coroutine
    def connect(self):
        self.stream = yield TCPClient().connect(self.host, self.port)
        timer = self.io_loop.call_at(self.io_loop.time() + 4, self.timeout_error)
        try:
            success_data = yield self.stream.read_until(b"\xcd\xea\xb3\xc9")
        except:
            return
        self.io_loop.remove_timeout(timer)

    @gen.coroutine
    def send_message_get_return(self, msg):
        yield self.connect()
        timer = self.io_loop.call_at(self.io_loop.time() + 6, self.timeout_error)
        if time.time() - self.accept_time > 1:
            print("%s--发送消息：" % datetime.datetime.now(), msg)
            self.lastsend_time = time.time()
            self.lastsend_msg = msg
            yield self.stream.write(transtoCode(msg['text']))
            try:
                rec_data = yield self.stream.read_until(b"\xcd\xea\xb3\xc9")
                if rec_data.startswith(b"CODE"):
                    rec_data = rec_data[:rec_data.find(b"\xcd\xea\xb3\xc9")]
                else:
                    rec_data = transformCodec(rec_data)
                    rec_data = rec_data[:rec_data.find("完成")]
            except:
                try:
                    resend_num = msg['resend_num']
                    msg['resend_num'] = resend_num+1
                except:
                    msg['resend_num'] = 1
                if msg['resend_num'] >= 3:
                    return "error"
                self.MSG_LIST.put(msg)
                return ""
        else:
            self.MSG_LIST.put(msg)
            rec_data = ""
        self.io_loop.remove_timeout(timer)
        self.stream.close()
        return rec_data

    @gen.coroutine
    def send_message_only(self, msg):
        yield self.connect()
        if time.time() - self.accept_time > 1:
            print("%s--发送消息：" % datetime.datetime.now(), msg)
            self.lastsend_time = time.time()
            self.lastsend_msg = msg
            yield self.stream.write(transtoCode(msg['text']))
        else:
            self.MSG_LIST.put(msg)
        self.stream.close()

    def timeout_error(self):
        print("TIMEOUT")
        self.stream.close()

    @gen.coroutine
    def send(self):
        print("启动客户端发消息协程")
        while True:
            if time.time() - self.accept_time > 1:
                msg = yield self.MSG_LIST.get()
                if msg["return"]:
                    msg_id = msg['id']
                    return_msg = yield self.send_message_get_return(msg)
                    if return_msg:
                        self.RETURN_MSG_LIST.append({"id": msg_id, "return_text": return_msg})
                else:
                    yield self.send_message_only(msg)
                yield gen.sleep(0.3)

    def sendmsg(self, msg):
        msg = {"text": msg, "return": False}
        self.MSG_LIST.put(msg)

    def sendmsg_getreturn(self, msg):
        id = time.time()
        msg = {"id": id, "text": msg, "return": True}
        self.MSG_LIST.put(msg)
        return self.get_return_msg(id)

    def get_return_msg(self, id):
        while True:
            for return_msg in self.RETURN_MSG_LIST[:]:
                if return_msg['id'] == id:
                    return return_msg['return_text']
            time.sleep(0.3)


