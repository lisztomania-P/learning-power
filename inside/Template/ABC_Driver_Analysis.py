#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/17
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : ABC_Driver_Analysis.py
# @Function : 驱动解析基类
from abc import abstractmethod
from urllib.parse import ParseResult

from inside.Config.System import SYSTEM
from inside.Template.Meta_Singleton import SINGLETON_ABC

__all__ = ['DRIVER_ANALYSIS']


class ABC_DRIVER_ANALYSIS(metaclass=SINGLETON_ABC):
    """驱动解析抽象类"""
    @abstractmethod
    def Master(self) -> ParseResult:
        """
        Url() -> ParseResult
        驱动集合链接

        :return: ParseResult
        """
        pass

    @abstractmethod
    def Download(self, system: SYSTEM) -> ParseResult:
        """
        Download() -> ParseResult
        驱动下载链接

        :param system: 系统
        :param version: 版本号
        :return: ParseResult
        """
        pass


class DRIVER_ANALYSIS(ABC_DRIVER_ANALYSIS):
    """驱动解析类实际继承类"""
    _map = {
        'linux': 'linux',
        'win32': 'win',
        'darwin': 'mac'
    }

    @property
    def Master(self) -> ParseResult:
        """
        Url -> ParseResult
        驱动集合链接

        :return: ParseResult
        """
        pass

    def Download(self, system: SYSTEM) -> ParseResult:
        """
        Download -> ParseResult
        驱动下载链接

        :param system: 系统
        :param version: 版本号
        :return: ParseResult
        """
        pass

