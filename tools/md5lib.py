#!/user/bin/env python
# -*- coding: utf-8 -*-
# @Time      : 2017/12/8/008 16:27
# @Author    : jiaojianglong

import hashlib


def md5(mingwen):
    m = hashlib.md5()
    mdr_str = mingwen.encode()
    m.update(mdr_str)
    ciphertext = m.hexdigest()
    return ciphertext


if __name__ == '__main__':
    print(md5('hahahahh'))
