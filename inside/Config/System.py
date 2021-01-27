#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : System.py
# @Function : 系统适配
import math
import sys
from typing import FrozenSet

from inside.Config.SystemArgs import WINDOWS, LINUX, MACOS
from inside.Template.ABC_System_Args import SYSTEM_ARGS

__all__ = ['SYSTEM']


class SYSTEM(SYSTEM_ARGS):
    """系统类"""
    __supports = frozenset({'linux', 'win32', 'darwin'})
    __supports_map = {
        'linux': 'Linux',
        'win32': 'Windows',
        'darwin': 'MacOs'
    }

    # 支持系统
    @property
    def Supports(self) -> FrozenSet:
        """
        Supports -> FrozenSet
        支持系统集合

        :return: FrozenSet
        """
        return self.__supports

    # 系统
    @property
    def Name(self) -> str:
        """
        Name -> str
        系统名称

        :return: str
        """
        return sys.platform

    # 位数
    @property
    def Bit(self) -> int:
        """
        Bit -> int
        系统位数

        :return: int
        """
        return int(math.log2(sys.maxsize + 1) + 1)

    # 系统参数
    @property
    def __System_Args(self) -> SYSTEM_ARGS:
        """
        __System_Args -> SYSTEM_ARGS
        获取当前操作系统类

        :return: SYSTEM_ARGS
        """
        if self.Name not in self.Supports:
            print(f"检测到运行环境为{self.Name}操作系统\n"
                  f"本程序暂不支持此系统\n"
                  f"仅支持{tuple(self.__supports_map.values())}")
            exit(code=0)
        else:
            if self.Name == 'win32':
                return WINDOWS()
            elif self.Name == 'linux':
                return LINUX()
            elif self.Name == 'darwin':
                return MACOS()

    @property
    def Clear(self) -> str:
        """
        Clear -> str
        清空控制台命令

        :return: str
        """
        return self.__System_Args.Clear

    @property
    def Driver(self) -> str:
        """
        Driver -> str
        驱动文件名称

        :return: str
        """
        return self.__System_Args.Driver

    @property
    def Driver_Chmod(self) -> str:
        """
        Driver_Chmod -> str
        添加驱动文件执行权限命令

        :return:
        """
        return self.__System_Args.Driver_Chmod

    @property
    def Chrome(self) -> bool:
        """
        Chrome -> bool
        谷歌浏览器是否安装

        :return: bool
        """
        return self.__System_Args.Chrome

    @property
    def Chrome_Version(self) -> str:
        """
        Chrome_Version -> str
        谷歌浏览器版本号

        :return: str
        """
        return self.__System_Args.Chrome_Version

    def Check_Chrome(self) -> None:
        """
        Check_Chrome() -> None
        检测谷歌浏览器是否安装，未安装则退出程序

        :return: None
        """
        if not self.Chrome:
            print("检测到谷歌浏览器未安装，无法进行本程序")
            exit(code=0)
