#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/26
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Mitmdump.py
# @Function : 拦截注入器
import subprocess

from inside.Config.Path import PATH
from inside.Template.Meta_Singleton import SINGLETON
__all__ = ['MITMDUMP']


class MITMDUMP(metaclass=SINGLETON):
    """拦截注入器"""
    __mitmdump: subprocess.Popen

    def __init__(self):
        """
        MITMDUMP()
        初始化

        """
        self.__self = '_'+type(self).__name__

    def Open(self) -> None:
        """
        Open() -> None
        打开

        :return: None
        """
        if not hasattr(self, self.__self+'__mitmdump') or self.__mitmdump.poll():
            self.__mitmdump = subprocess.Popen('mitmdump -q -p 8080 -s '+PATH().Intercept)

    def Close(self) -> None:
        """
        Close() -> None
        关闭

        :return: None
        """
        if hasattr(self, self.__self+'__mitmdump'):
            self.__mitmdump.kill()
