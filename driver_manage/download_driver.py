#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/12
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : download_driver.py
# @Function : 驱动下载
import os
import hashlib
import requests
import glob
from typing import List
from bs4 import BeautifulSoup
from config.system_config import CONSOLE_CLEAR, SYSTEM_BIT
from config.driver_config import DRIVER_NAME, DRIVER_LINK, DRIVER_LIST_LINK
from config.path_config import DRIVER_FILES, DRIVER_DIR
from requests.models import Response
from bs4.element import Tag
from driver_manage import download_bar

__download_link: str
__file_md5: str


def chrome_version():
    msg = '''{version}输入Chrome版本
        获取方法：
            1、打开浏览器输入：chrome://version/
            2、复制<Google Chrome:>后面的版本号，如<87.0.4280.88>
            3、粘贴于此:'''
    msg_temp = msg.format(version='')
    while True:
        os.system(CONSOLE_CLEAR)
        version: str = input(msg_temp).strip().replace(' ', '')
        check: int = __check_version(version=version)
        if check != -1:
            link: str = DRIVER_LIST_LINK.format(version=version)
            test_link: Response = requests.get(url=link)
            if __analysis_xml(text=test_link.text, version=check):
                __decision_download()
                break
            else:
                msg_temp = msg.format(
                    version=f"版本:<{version}>未找到，请重新输入！！！\n"
                )
        else:
            msg_temp = msg.format(
                version=f"版本:<{version}>格式错误，请重新输入！！！\n"
            )


def __check_version(version: str) -> int:
    try:
        temp: int = int(version[:version.find('.')])
        if temp == 2:
            return 1
        elif temp >= 70:
            return 2
    except ValueError:
        return -1


def __analysis_xml(text: str, version: int) -> bool:
    soup = BeautifulSoup(text, 'xml')
    keys: List[Tag] = soup.find_all(name='Contents')
    if len(keys):
        for key in keys:
            link: str = key.find(name='Key').text
            temp = DRIVER_NAME
            if version == 1 and temp == 'linux':
                temp += SYSTEM_BIT[:SYSTEM_BIT.find('b')]
            if temp in link:
                global __download_link
                global __file_md5
                __download_link = link
                __file_md5 = eval(key.find(name='ETag').text)
                return True
    else:
        return False


def __check_zip_md5() -> bool:
    file = glob.glob(DRIVER_FILES)
    if file:
        temp = file[0]
        with open(temp, 'rb') as f:
            data = f.read()
            f.close()
        data_md5 = hashlib.md5(data).hexdigest()
        if data_md5 == __file_md5:
            return True
        else:
            os.remove(temp)
            return False
    else:
        return False


def __decision_download():
    if not __check_zip_md5():
        __download_driver()


def __download_driver():
    link = DRIVER_LINK+__download_link
    file_name = __download_link.split('/')[-1]
    file_name = os.path.join(DRIVER_DIR, file_name)
    download_bar.download(url=link, dst=file_name)
