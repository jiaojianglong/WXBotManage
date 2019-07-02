#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7
# @Author  : JiaoJianglong

import re


def transformCodec(re_data):
    try:
        re_data = re_data.decode('gbk')
    except Exception as error:

        pos = re.findall(r'position([\d]+):', str(error).replace(' ', ''))
        if len(pos) == 1:
            re_data = re_data[0:int(pos[0])] + re_data[int(pos[0]) + 1:]
            re_data = transformCodec(re_data)
            return re_data
    return re_data


def transtoCode(re_data):
    try:
        re_data = re_data.encode('gbk')
    except Exception as error:

        pos = re.findall(r'position([\d]+):', str(error).replace(' ', ''))
        if len(pos) == 1:
            re_data = re_data[0:int(pos[0])] + re_data[int(pos[0]) + 1:]
            re_data = transtoCode(re_data)
            return re_data
    return re_data
