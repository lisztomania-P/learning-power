#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : QR_Vessel.py
# @Function : 二维码容器
from inside.Driver.Driver_Manage import DRIVER_MANAGE
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['QR_VESSEL']


class QR_VESSEL(metaclass=SINGLETON):
    """二维码容器类"""

    def __init__(self):
        """
        QR_VESSEL()
        初始化

        """
        self.__driver = DRIVER_MANAGE().QR

    def Show_QR(self, qr: str):
        """
        Show_QR(qr: str) -> None
        显示二维码

        :param qr: 图片二维码，格式为：data:image/png;base64,xxx==
        :return: None
        """
        js = "document.body.innerHTML='';"
        js += f'''
        var qr = document.createElement("img");
        qr.src="{qr}";
        document.body.appendChild(qr);'''
        self.__driver.execute_script(script=js)

    def QR_QUIT(self) -> str:
        """
        QR_QUIT() -> str
        二维码容器退出

        :return: str
            Success: 退出成功
            Nonexistence: 不存在任务浏览器
        """
        return DRIVER_MANAGE().QR_Quit

    def __del__(self) -> str:
        return DRIVER_MANAGE().QR_Quit


