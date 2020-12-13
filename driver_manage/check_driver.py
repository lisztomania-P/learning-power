#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/12
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : check_driver.py
# @Function : 检测驱动

import os
import glob
import zipfile
from driver_manage.download_driver import chrome_version
from config.path_config import DRIVER_FILE, DRIVER_FILES, DRIVER_DIR


def check_driver() -> bool:
    temp = glob.glob(DRIVER_FILE)
    if not temp and not __unzip_files():
        chrome_version()
        __unzip_files()
        return True
    else:
        return False


def __unzip_files() -> bool:
    temp = glob.glob(DRIVER_FILES)
    if temp:
        for f in temp:
            if zipfile.is_zipfile(f):
                files = zipfile.ZipFile(temp[0])
                if not files.testzip():
                    files.extractall(path=DRIVER_DIR)
                    return True
                else:
                    os.remove(f)
                    return False
            else:
                os.remove(f)
                return False
    else:
        return False
