#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : SystemArgs.py
# @Function : 系统参数
from inside.Template.ABC_System_Args import SYSTEM_ARGS

__all__ = ['WINDOWS', 'LINUX', 'MACOS']


class WINDOWS(SYSTEM_ARGS):
    """Windows操作系统类"""

    def __init__(self):
        """
        WINDOWS()
        初始化

        """
        import winreg
        self.__winreg = winreg
        self.__winreg_key = self.__winreg.OpenKey(
            key=self.__winreg.HKEY_CURRENT_USER,
            sub_key=r'Software\Google\Chrome\BLBeacon')

    @property
    def Clear(self) -> str:
        """
        Clear -> str
        清空控制台命令

        :return: str
        """
        return 'cls'

    @property
    def Driver(self) -> str:
        """
        Driver -> str
        驱动文件名称

        :return: str
        """
        return 'chromedriver.exe'

    @property
    def Driver_Chmod(self) -> str:
        """
        Driver_Chmod -> str
        添加驱动文件执行权限命令

        :return: str
        """
        return ''

    @property
    def Chrome(self) -> bool:
        """
        Chrome -> bool
        谷歌浏览器是否安装

        :return: bool
        """
        try:
            return isinstance(self.Chrome_Version, str)
        except FileNotFoundError:
            return False

    @property
    def Chrome_Version(self) -> str:
        """
        Chrome_Version -> str
        谷歌浏览器版本号

        :return: str
        """
        return self.__winreg.QueryValueEx(
            self.__winreg_key,
            'version'
        )[0]


class LINUX(SYSTEM_ARGS):
    """Linux操作系统类"""

    def __init__(self):
        """
        LINUX()
        初始化

        """
        import os
        self.__os = os

    @property
    def Clear(self) -> str:
        """
        Clear -> str
        清空控制台命令

        :return: str
        """
        return 'clear'

    @property
    def Driver(self) -> str:
        """
        Driver -> str
        驱动文件名称

        :return: str
        """
        return 'chromedriver'

    @property
    def Driver_Chmod(self) -> str:
        """
        Driver_Chmod -> str
        添加驱动文件执行权限命令

        :return: str
        """
        return 'chmod +x '

    @property
    def Chrome(self) -> bool:
        """
        Chrome -> bool
        谷歌浏览器是否安装

        :return: bool
        """
        try:
            return isinstance(self.Chrome_Version, str)
        except IndexError:
            return False

    @property
    def Chrome_Version(self) -> str:
        """
        Chrome_Version -> str
        谷歌浏览器版本号

        :return: str
        """
        version = self.__os.popen(cmd='google-chrome --version').readline()
        return version.strip().split()[-1]


class MACOS(SYSTEM_ARGS):
    """MacOs操作系统类"""

    def __init__(self):
        """
        MACOS()
        初始化

        """
        import os
        self.__os = os

    @property
    def Clear(self) -> str:
        """
        Clear -> str
        清空控制台命令

        :return: str
        """
        return 'clear'

    @property
    def Driver(self) -> str:
        """
        Driver -> str
        驱动文件名称

        :return: str
        """
        return 'chromedriver'

    @property
    def Driver_Chmod(self) -> str:
        """
        Driver_Chmod -> str
        添加驱动文件执行权限命令

        :return: str
        """
        return 'chmod +x '

    @property
    def Chrome(self) -> bool:
        """
        Chrome -> bool
        谷歌浏览器是否安装

        :return: bool
        """
        try:
            return isinstance(self.Chrome_Version, str)
        except IndexError:
            return False

    @property
    def Chrome_Version(self) -> str:
        """
        Chrome_Version -> str
        谷歌浏览器版本号

        :return: str
        """
        version = self.__os.popen(cmd=r'/Applications/Google\ '
                                      r'Chrome.app/Contents/MacOS/Google\ '
                                      r'Chrome --version').readline()
        return version.strip().split()[-1]
