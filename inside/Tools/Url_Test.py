#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/28
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Url_Test.py
# @Function : 链接延迟测试
import time
import ssl
from socket import timeout
from urllib import request
from urllib.error import URLError

from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['URL_TEST', 'Url_Test']


class URL_TEST(metaclass=SINGLETON):
    """url延迟测试类"""
    ssl._create_default_https_context = ssl._create_unverified_context

    @classmethod
    def Url_Test(cls, url: str) -> float:
        """
        Url_Test(url: str) -> float
        测试url访问延迟

        :param url: url
        :return: float
        """
        try:
            temp = 0
            for _ in range(3):
                s = time.time()
                try:
                    request.urlopen(url=url, timeout=3)
                except (timeout, URLError):
                    pass
                temp += time.time() - s
            return temp / 3
        except (ValueError, AttributeError):
            raise Exception(f"{url}:不是正确的url链接")


_inst = URL_TEST
Url_Test = _inst.Url_Test
