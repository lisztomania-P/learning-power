#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/16
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Driver_Check.py
# @Function : 驱动检测
import os

from inside.Config.Path import PATH
from inside.Config.System import SYSTEM
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['DRIVER_CHECK']


class DRIVER_CHECK(metaclass=SINGLETON):
    """驱动检测类"""
    @property
    def Dir(self) -> bool:
        """
        Dir -> bool
        驱动目录是否存在

        :return: bool
        """
        return os.path.exists(PATH().Driver)

    @property
    def File(self) -> bool:
        """
        File -> bool
        驱动文件是否存在

        :return: bool
        """
        return os.path.exists(PATH().Driver_File)

    @property
    def Version(self) -> str:
        """
        Version -> str
        驱动支持谷歌浏览器版本号

        :return: str
        """
        cmd = PATH().Driver_File + ' --version'
        version = os.popen(cmd=cmd).readline()
        version = version.strip().split()
        return version[1]

    @property
    def Execute_Permission(self) -> bool:
        """
        Execute_Permission -> bool
        驱动程序是否有执行权限

        :return: bool
        """
        try:
            isinstance(self.Version, str)
            return True
        except IndexError:
            return False

    def Driver_Chrome_Version(self, system: SYSTEM) -> bool:
        """
        Driver_Chrome_Version(system: SYSTEM) -> bool
        驱动程序是否支持谷歌浏览器版本

        :param system: 系统类
        :return: bool
        """
        driver_version = self.Version.split('.')[:3]
        chrome_version = system.Chrome_Version.split('.')[:3]
        return driver_version == chrome_version

    def Add_Execute_Permission(self, system: SYSTEM) -> bool:
        """
        Add_Execute_Permission -> bool
        为驱动程序添加执行权限

        :param system: 系统类
        :return: bool
        """
        command = system.Driver_Chmod+PATH().Driver_File
        if command != PATH().Driver_File:
            return os.system(command=command) == 0
        return True

