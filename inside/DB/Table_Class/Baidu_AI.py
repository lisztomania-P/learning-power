#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/2/6
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Baidu_AI.py
# @Function : 百度AI类
__all__ = ['BAIDU_AI']


class BAIDU_AI(object):
    """百度AI类"""

    def __init__(self, ak: str, sk: str):
        """
        BAIDU_AI(ak: str, sk: str)
        初始化

        @param ak: API Key
        @param sk: Secret Key
        """
        self.__ak = ak
        self.__sk = sk

    @property
    def Ak(self) -> str:
        """
        Ak -> str

        @return: API Key
        """
        return self.__ak

    @Ak.setter
    def Ak(self, ak: str) -> None:
        """
        Ak = ak: str

        @param ak: API Key
        @return: None
        """
        self.__ak = ak

    @property
    def Sk(self) -> str:
        """
        Sk -> str

        @return: Secret Key
        """
        return self.__sk

    @Sk.setter
    def Sk(self, sk: str) -> None:
        """
        Sk = sk: str

        @param sk: Secret Key
        @return: None
        """
        self.__sk = sk
