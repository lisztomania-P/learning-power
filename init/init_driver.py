#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/1
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : init_driver.py
# @Function : 初始化驱动

import os
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from config.path_config import DRIVER_FILE, DB_TEMP_DIR
from config.driver_config import DRIVER_OPTIONS
from config.system_config import CONSOLE_CLEAR
from driver_manage.check_driver import check_driver


def __set_driver():
    check_driver()
    os.system(CONSOLE_CLEAR)
    auto = input("执行视频是否静音(Y/n):")
    display = input("是否显示自动化过程(y/N):")
    print("稍等一会儿，正在连接服务器（等待时间主要取决于网速，其次是电脑性能）！")
    if auto in ['y', 'Y', '']:
        DRIVER_OPTIONS[1][1] = True
    else:
        DRIVER_OPTIONS[1][1] = False
    if display in ['y', 'Y']:
        DRIVER_OPTIONS[2][1] = True
    else:
        DRIVER_OPTIONS[2][1] = False


def driver() -> WebDriver:
    __set_driver()
    # 驱动配置
    caps = {
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
                        "download.default_directory": DB_TEMP_DIR,
                        # 自动下载
                        "download.prompt_for_download": False
                    },
                'excludeSwitches': [
                    # 不显示日志
                    'enable-logging',
                    # 规避检测
                    'enable-automation'
                    ],
                'args':
                    [],
                'perfLoggingPrefs':
                    {
                        # 开启network日志
                        'enableNetwork': True
                    },
                'w3c': False
            }
    }
    # 静音
    if DRIVER_OPTIONS[1][1]:
        caps['goog:chromeOptions']['args'].append("--mute-audio")
    # 无窗口化
    if not DRIVER_OPTIONS[2][1]:
        caps['goog:chromeOptions']['args'].append("--headless")
    driver = webdriver.Chrome(
        desired_capabilities=caps,
        executable_path=DRIVER_FILE,
    )
    return driver
