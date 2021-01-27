#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Task.py
# @Function : 任务类
from typing import Union

__all__ = ['TASK']


class TASK(object):
    """任务类"""

    def __init__(self, link: str, isread: Union[int, bool]):
        """
        TASK(link: str, isread: Union[int, bool])
        初始化

        :param link: 链接
        :param isread: 是否已读
        """

        self.__link = link
        self.__isread = self.__Is_Read(isread=isread)

    @property
    def Link(self) -> str:
        """
        Link -> str
        链接

        :return: str
        """
        return self.__link

    @property
    def Is_Read(self) -> bool:
        """
        Is_Read -> bool
        是否已读

        :return: bool
        """
        return self.__isread

    @Is_Read.setter
    def Is_Read(self, isread: Union[int, bool]) -> None:
        """
        Is_Read -> None
        设置是否已读

        :param isread: Union[int, bool]
        :return: None
        """
        self.__isread = self.__Is_Read(isread=isread)

    @classmethod
    def __Is_Read(cls, isread: Union[int, bool]) -> bool:
        """
        __Is_Read(isread: Union[int, bool]) -> bool
        设定是否已读，由于数据库内不能存储布尔值，所以由0/1代替；
        因此数字只限定0/1

        :param isread: 1/0 or bool
        :return: bool
        """
        if isinstance(isread, bool):
            return isread
        elif isinstance(isread, int):
            if isread in (0, 1):
                return True if isread else False
            else:
                raise Exception('isread must be 0 or 1')

    @property
    def Is_Read_DB(self) -> int:
        """
        Is_Read_DB -> int
        是否已读(数据库读取接口，返回1/0)

        :return: int
        """
        return 1 if self.__isread else 0
