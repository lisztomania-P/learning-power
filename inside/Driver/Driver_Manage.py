#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/16
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Driver_Manage.py
# @Function : 驱动管理
import os

from selenium.webdriver.chrome.webdriver import WebDriver

from inside.Config.Api import API
from inside.Config.Path import PATH
from inside.Config.System import SYSTEM
from inside.Driver.Driver_Check import DRIVER_CHECK
from inside.Driver.Driver_Download import DRIVER_DOWNLOAD
from inside.Driver.Driver_Init import DRIVER_INIT
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['DRIVER_MANAGE']


class DRIVER_MANAGE(metaclass=SINGLETON):
    """驱动管理类"""

    def __init__(self):
        """
        初始化时会要求设置选项
        """
        self.__Driver_Check()

    @classmethod
    def __Check_Dir(cls) -> bool:
        """
        Check_Dir() -> None
        检测驱动目录是否存在，如不存在则自动创建

        :return: bool
        """
        if not DRIVER_CHECK().Dir:
            print(f"检测到驱动目录未创建\n"
                  f"自动创建中")
            os.mkdir(PATH().Driver)
            print(f"驱动目录为{PATH().Driver}")
            return False
        return True

    def __Driver_Check(self) -> None:
        """
        __Driver_Check() -> None
        驱动检查，确保驱动能够正常使用

        :return: None
        """
        temp = False
        if not temp and not self.__Check_Dir():
            temp = True
        if not temp and not DRIVER_CHECK().File:
            print(f"检测到驱动未下载")
            temp = True
        if not temp and not DRIVER_CHECK().Driver_Chrome_Version(
                system=SYSTEM()):
            print(f"检测到驱动不支持本机Chrome")
            temp = True
        if temp:
            print(f"驱动自动下载中")
            size = DRIVER_DOWNLOAD().Download(
                link=API().Driver.Download(system=SYSTEM()))
            print(f"驱动自动下载完毕\n"
                  f"文件大小为{size / 1024 / 1024}MB")
        if not DRIVER_CHECK().Execute_Permission:
            print(f"检测到驱动没有执行权限\n"
                  f"自动添加执行权限")
            DRIVER_CHECK().Add_Execute_Permission(system=SYSTEM())
            print(f"添加执行权限完毕")

    @property
    def Task(self) -> WebDriver:
        """
        Task -> WebDriver
        任务浏览器驱动器，关闭时，请务必使用Task_Quit

        :return: WebDriver
        """
        return DRIVER_INIT().Task_Driver

    @property
    def Task_Quit(self) -> str:
        """
        Task_Quit -> str
        任务浏览器驱动器关闭

        :return: str
        """
        return DRIVER_INIT().Task_Quit

    @property
    def QR(self) -> WebDriver:
        """
        QR -> WebDriver
        二维码浏览器驱动器，关闭时，请务必使用QR_Quit

        :return: WebDriver
        """
        return DRIVER_INIT().QR_Driver

    @property
    def QR_Quit(self) -> str:
        """
        QR_Quit -> str
        二维码浏览器驱动器关闭

        :return: str
            Success: 退出成功
            Nonexistence: 不存在任务浏览器
        """
        return DRIVER_INIT().QR_Quit
