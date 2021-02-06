#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/14
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Path.py
# @Function : 路径配置文件
import os

from inside.Config.System import SYSTEM
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['PATH']


class PATH(metaclass=SINGLETON):
    """路径类"""

    def __init__(self):
        """
        PATH()
        初始化，配置文件绝对路径

        """
        self.__Config_Path: str = os.path.dirname(os.path.abspath(__file__))

    @property
    def Base(self) -> str:
        """
        Base -> str
        项目绝对路径

        :return: str
        """
        return os.path.dirname(os.path.dirname(self.__Config_Path))

    @property
    def Driver(self) -> str:
        """
        Driver -> str
        驱动目录绝对路径

        :return: str
        """
        return os.path.join(self.Base, 'Driver')

    @property
    def Driver_File(self) -> str:
        """
        Driver_File -> str
        驱动文件绝对路径

        :return: str
        """
        return os.path.join(self.Driver, SYSTEM().Driver)

    @property
    def DB(self) -> str:
        """
        DB -> str
        数据库目录绝对路径

        :return: str
        """
        return os.path.join(self.Base, 'DB')

    @property
    def DB_File(self) -> str:
        """
        DB_File -> str
        数据库文件绝对路径

        :return: str
        """
        return os.path.join(self.DB, 'db.db')

    @property
    def Temp(self) -> str:
        """
        Temp -> str
        临时文件绝对路径

        :return: str
        """
        return os.path.join(self.Base, 'Temp')

    @property
    def Intercept(self) -> str:
        """
        Intercept -> str
        拦截注入脚本绝对路径

        :return: str
        """
        xt = SYSTEM().System
        temp = os.path.join(os.path.dirname(self.__Config_Path), 'Task')
        temp = os.path.join(temp, 'Mitmdump')
        temp = os.path.join(temp, 'Intercept')
        temp = os.path.join(temp, 'Script.py')
        if xt == 'macOs':
            temp = temp.replace(os.path.expanduser('~'), '~')
        return temp
