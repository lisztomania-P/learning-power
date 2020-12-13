#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/12
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : driver_config.py
# @Function : 驱动配置文件

from typing import Dict
from config.system_config import SYSTEM_NAME

# 驱动名称
_DRIVER_NAME_DICT: Dict = {
    'win32': 'win',
    'linux': 'linux',
    'darwin': 'mac'
}
DRIVER_NAME: str = _DRIVER_NAME_DICT[SYSTEM_NAME]
# 驱动后缀
DRIVER_SUFFIX: str = '.exe' if DRIVER_NAME == 'win' else ''
# 驱动首页
DRIVER_LINK: str = 'http://chromedriver.storage.googleapis.com/'
# 驱动列表链接（正式）
DRIVER_LIST_LINK: str = 'http://chromedriver.storage.googleapis.com/?delimiter=/&prefix={version}/'


# 驱动配置
DRIVER_OPTIONS: Dict = {
    1: ['静音', True],
    2: ['显示', False]
}