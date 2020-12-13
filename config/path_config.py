#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/13
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : path_config.py
# @Function : 路径配置
import os
from config.driver_config import DRIVER_SUFFIX
# 项目目录
BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
# 数据目录
DB_DIR: str = os.path.join(BASE_DIR, '../db')
# 数据库文件
DB_FILE_DIR: str = os.path.join(DB_DIR, 'tasks.db')
# 驱动目录
DRIVER_DIR: str = os.path.join(BASE_DIR, '../driver')
# 驱动压缩文件
DRIVER_FILES: str = os.path.join(DRIVER_DIR, 'chromedriver*.zip')
# 驱动文件
DRIVER_FILE: str = os.path.join(DRIVER_DIR, 'chromedriver'+DRIVER_SUFFIX)
# 临时数据目录
DB_TEMP_DIR: str = os.path.join(DB_DIR, 'temp')
# 临时JSON文件匹配
DB_TEMP_DIR_JSON: str = os.path.join(DB_TEMP_DIR, '*.json')