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
from configuration import DRIVER_FILE_PATH, DB_TEMP_DIR, DRIVER_OPTIONS


def __set_driver():
    os.system('cls')
    auto = input("执行视频是否静音(y/n):")
    display = input("是否显示自动化过程(y/n):")
    if auto in ['y', 'Y']:
        DRIVER_OPTIONS[1][1] = True
    else:
        DRIVER_OPTIONS[1][1] = False
    if display in ['y', 'Y']:
        DRIVER_OPTIONS[2][1] = True
    else:
        DRIVER_OPTIONS[2][1] = False


def Driver() -> WebDriver:
    __set_driver()
    chrome_profile = webdriver.ChromeOptions()
    # 下载相关
    prefs = {"download.default_directory": DB_TEMP_DIR,
             "download.prompt_for_download": False}
    chrome_profile.add_experimental_option("prefs", prefs)
    # 静音
    if DRIVER_OPTIONS[1][1]:
        chrome_profile.add_argument("--mute-audio")
    # 无窗口化
    if not DRIVER_OPTIONS[2][1]:
        chrome_profile.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=DRIVER_FILE_PATH,
                              options=chrome_profile)
    return driver
