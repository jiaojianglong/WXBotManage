#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/10/14 0014 19:15
# @Author  : jiaojianglong

import json
import requests
from tools.md5lib import md5

def tuling_replay(kwargs,msg):

    body = {
            "reqType":kwargs['msg_type'],#输入类型:0-文本(默认)、1-图片、2-音频
            "perception": {
                "selfInfo": {
                    "location": {
                    }
                }
            },
            "userInfo": {
                "apiKey": "476fba18fe1d41a7bf652ff37a9c5295",
                "userId": md5(kwargs['user_id']),
                "groupId":"",#群聊id
                "userIdName":""#用户群内名称
            }
        }

    if kwargs.get("text",""):
        body["perception"].update(dict(inputText={"text": kwargs['text']},))
    if kwargs.get("imageUrl",""):
        body["perception"].update(dict(inputImage={"url": kwargs['imageUrl']}, ))
    if kwargs.get("mediaUrl",""):
        body["perception"].update(dict(inputMedia={"url": kwargs['mediaUrl']}, ))

    if kwargs.get("group_id",""):
        body["userInfo"]['groupId'] = kwargs['group_id']
    if kwargs.get("user_nick_name",""):
        body["userInfo"]['userIdName'] = kwargs['user_nick_name']

    location = kwargs.get("location",{})
    if location.get("province",""):
        body["perception"]['selfInfo']['location'].update(dict(province=location['province']))
    if location.get("city", ""):
        body["perception"]['selfInfo']['location'].update(dict(province=location['city']))
    if location.get("street", ""):
        body["perception"]['selfInfo']['location'].update(dict(province=location['street']))


    print("图灵请求参数：",body)
    res = requests.post("http://openapi.tuling123.com/openapi/api/v2", json=body).text
    res = json.loads(res)
    print("图灵返回：",res)

    results = res["results"]
    for result in results:
        if result["resultType"] == "text":
            msg.reply_text(result["values"]['text'])
        elif result['resultType'] == "url":
            msg.reply_text(result["values"]['url'])
        elif result['resultType'] == "voice":
            print("图灵返回音频")
        elif result['resultType'] == "video":
            print("图灵返回视频")
        elif result['resultType'] == "image":
            image_url = result["values"]['image']
            image_name = image_url.split("com/")[1]
            msg.sendImage(image_name,image_url)
        elif result['resultType'] == "news":
            print("图灵返回图文消息")
