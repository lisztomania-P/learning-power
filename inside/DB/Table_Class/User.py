#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : User.py
# @Function : 用户类
from datetime import datetime
from typing import Dict

__all__ = ['USER']


class USER(object):
    """用户类"""

    def __init__(self, user_id: int, token: str):
        """
        USER(user_id: int, token: str)
        初始化

        :param user_id: 用户ID
        :param token: 令牌
        """
        self.__user_id = user_id
        self.__token = token
        self.__time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @property
    def Id(self) -> int:
        """
        Id -> int
        名称

        :return: int
        """
        return self.__user_id

    @property
    def Token(self) -> str:
        """
        Token -> str
        令牌

        :return: str
        """
        return self.__token

    @property
    def Token_Driver(self) -> Dict:
        """
        Token_Driver -> Dict
        驱动令牌，格式为:{'domain': '.xuexi.cn', 'name': 'token', 'value': 'token'}

        :return: Dict
        """
        return {'domain': '.xuexi.cn', 'name': 'token', 'value': self.Token}

    @property
    def Time(self) -> str:
        """
        Time -> str
        对象创建时间戳

        :return: str
        """
        return self.__time
