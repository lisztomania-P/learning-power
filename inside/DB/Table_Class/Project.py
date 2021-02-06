#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/2/6
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Project.py
# @Function : 专项答题类
__all__ = ['PROJECT']


class PROJECT(object):

    def __init__(self, pid: int):
        """
        PROJECT(pid: int)
        初始化

        @param pid: 专项答题ID
        """
        self.__pid = pid

    @property
    def Id(self) -> int:
        """
        Id -> int

        @return: 专项答题ID
        """
        return self.__pid
