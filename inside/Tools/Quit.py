#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/25
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Quit.py
# @Function : 退出
from inside.DB.DB_Manage import DB_MANAGE
from inside.Driver.Driver_Manage import DRIVER_MANAGE
from inside.Task.Mitmdump.Mitmdump import MITMDUMP
from inside.Tools.Network import NETWORK

__all__ = ['Quit']


def Quit() -> None:
    """
    Quit() -> None
    有序退出程序

    :return: None
    """
    NETWORK().Quit()
    temp = DRIVER_MANAGE().Task_Quit
    DB_MANAGE().Quit()
    MITMDUMP().Close()
    del temp

