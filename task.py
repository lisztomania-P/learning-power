#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/10
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : task.py
# @Function : 任务父类


class Task(object):
    __id: int
    __itemId: str
    __url: str
    __see: bool

    def __init__(self, itemId: str, url: str, see: bool):
        self.itemId = itemId
        self.url = url
        self.see = see

    @property
    def id(self) -> int:
        try:
            return self.__id
        except AttributeError:
            return 0

    @id.setter
    def id(self, iid: int):
        if isinstance(iid, int):
            self.__id = iid
        else:
            raise Exception("id must be an int")

    @property
    def itemId(self) -> str:
        return self.__itemId

    @itemId.setter
    def itemId(self, itemId: str):
        if isinstance(itemId, str):
            self.__itemId = itemId
        else:
            raise Exception("itemId must be an str")

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, url: str):
        if isinstance(url, str):
            self.__url = url
        else:
            raise Exception("url must be an str")

    @property
    def see(self) -> bool:
        return self.__see

    @see.setter
    def see(self, see: bool):
        if isinstance(see, bool):
            self.__see = see
        else:
            raise Exception("see must be an bool")
