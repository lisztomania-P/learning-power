#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/2/6
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : ABC_Answer.py
# @Function : 答题抽象类
from abc import abstractmethod
from typing import Dict

from inside.Template.Meta_Singleton import SINGLETON_ABC
__all__ = ['ABC_ANSWER']


class ABC_ANSWER(metaclass=SINGLETON_ABC):
    """答题抽象类"""

    @abstractmethod
    def Url_Put(self, url: str) -> bool:
        """
        Url_Put(url: str) -> bool
        提交判断

        :param url: url
        :return: bool
        """
        pass

    @abstractmethod
    def Url_Res(self, url: str) -> bool:
        """
        Url_Res(url: str) -> bool
        答案判断

        :param url: url
        :return: bool
        """
        pass

    @abstractmethod
    def Extract(self, data: bytes) -> Dict:
        """
        Extract(data: bytes) -> Dict
        提取答案

        :param data: 包含答案的字节数据
        :return: Dict
        """
        pass

    @abstractmethod
    def Inject(self, data: bytes, res: Dict) -> bytes:
        """
        Inject(data: bytes, res: Dict) -> bytes
        注入答案

        :param data: 原始提交数据
        :param res: 包含答案数据
        :return: 修改后的提交数据
        """
        pass
