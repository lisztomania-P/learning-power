#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/16
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Driver_Init.py
# @Function : 驱动初始化
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.webdriver import WebDriver

from inside.Options.Options import OPTIONS
from inside.Config.Path import PATH
from inside.Config.User_Agent import USER_AGENT
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['DRIVER_INIT']


class DRIVER_INIT(metaclass=SINGLETON):
    """驱动初始化类"""
    __instances = {}

    def __init__(self):
        """初始化驱动配置文件"""
        self.__config = {
            'browserName': 'chrome',
            # network日志相关
            'loggingPrefs':
                {
                    'browser': 'ALL',
                    'driver': 'ALL',
                    'performance': 'ALL'
                },
            'goog:chromeOptions':
                {
                    'prefs':
                        {
                            # 默认下载目录
                            "download.default_directory": PATH().Temp,
                            # 自动下载
                            "download.prompt_for_download": False,
                            # 无图模式
                            "profile.managed_default_content_settings.images": 2
                        },
                    'excludeSwitches': [
                        # 不显示日志
                        'enable-logging',
                        # 规避检测
                        'enable-automation'
                        ],
                    'args':
                        [
                            # 浏览器标识
                            '--user-agent=' + USER_AGENT().User_Agent,
                            # 本地代理
                            '--proxy-server=127.0.0.1:8080',
                            # 忽略证书问题
                            '--ignore-certificate-errors'
                        ],
                    'perfLoggingPrefs':
                        {
                            # 开启network日志
                            'enableNetwork': True
                        },
                    'w3c': False
                }
        }
        self.__Check_Options()

    def __Check_Options(self) -> None:
        """
        __Check_Options() -> None
        检查选项，根据选项初始化配置文件

        :return: None
        """
        temp = []
        if OPTIONS().Mute_Audio:
            self.__config['goog:chromeOptions']['args'].append("--mute-audio")
        if OPTIONS().Headless:
            self.__config['goog:chromeOptions']['args'].append("--headless")

    @property
    def Task_Driver(self) -> WebDriver:
        """
        Task_Driver -> WebDriver
        任务浏览器，根据配置文件生成

        :return: WebDriver
        """
        if not self.__instances.get('Task'):
            self.__instances['Task'] = Chrome(
                desired_capabilities=self.__config,
                executable_path=PATH().Driver_File
            )
        return self.__instances['Task']

    @property
    def Task_Quit(self) -> str:
        """
        Task_Quit -> str
        任务浏览器退出

        :return: str
            Success: 退出成功
            Nonexistence: 不存在任务浏览器
        """
        if self.__instances.get('Task'):
            self.__instances['Task'].quit()
            self.__instances.pop('Task')
            return 'Success'
        return 'Nonexistence'

    @property
    def QR_Driver(self) -> WebDriver:
        """
        Task_Driver -> WebDriver
        二维码浏览器，根据默认配置文件生成

        :return: WebDriver
        """
        if not self.__instances.get('QR'):
            self.__instances['QR'] = Chrome(
                executable_path=PATH().Driver_File
            )
            self.__instances['QR'].set_window_size(width=50, height=350)
        return self.__instances['QR']

    @property
    def QR_Quit(self) -> str:
        """
        Task_Quit -> str
        二维码浏览器退出

        :return: str
            Success: 退出成功
            Nonexistence: 不存在任务浏览器
        """
        if self.__instances.get('QR'):
            self.__instances['QR'].quit()
            self.__instances.pop('QR')
            return 'Success'
        return 'Nonexistence'
