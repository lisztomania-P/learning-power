#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : ABC_System_Args.py
# @Function : 系统基类
from abc import abstractmethod

from inside.Template.Meta_Singleton import SINGLETON_ABC

__all__ = ["SYSTEM_ARGS"]


class ABC_SYSTEM_ARGS(metaclass=SINGLETON_ABC):
    """抽象系统类"""

    @abstractmethod
    def Clear(self) -> str:
        """
        Clear() -> str
        清空控制台命令

        :return: str
        """
        pass

    @abstractmethod
    def Driver(self) -> str:
        """
        Driver() -> str
        驱动文件名称

        :return: str
        """
        pass

    @abstractmethod
    def Driver_Chmod(self) -> str:
        """
        Driver_Chmod() -> str
        添加驱动文件执行权限命令

        :return: str
        """
        pass

    @abstractmethod
    def Chrome(self) -> bool:
        """
        Chrome() -> bool
        谷歌浏览器是否安装

        :return: bool
        """
        pass

    @abstractmethod
    def Chrome_Version(self) -> str:
        """
        Chrome_Version() -> str
        谷歌浏览器版本号

        :return: str
        """
        pass


class SYSTEM_ARGS(ABC_SYSTEM_ARGS):
    """系统实际继承类，使每个方法都变为属性"""

    @property
    def Clear(self) -> str:
        """
        Clear -> str
        清空控制台命令

        :return: str
        """
        pass

    @property
    def Driver(self) -> str:
        """
        Driver -> str
        驱动文件名称

        :return: str
        """
        pass

    @property
    def Driver_Chmod(self) -> str:
        """
        Driver_Chmod -> str
        添加驱动文件执行权限命令

        :return: str
        """
        pass

    @property
    def Chrome(self) -> bool:
        """
        Chrome -> bool
        谷歌浏览器是否安装

        :return: bool
        """
        pass

    @property
    def Chrome_Version(self) -> str:
        """
        Chrome_Version -> str
        谷歌浏览器版本号

        :return: str
        """
        pass

