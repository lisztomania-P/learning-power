#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/13
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : system_config.py
# @Function : 系统适配

import sys
import platform
from typing import Dict

# 系统名称
SYSTEM_NAME: str = sys.platform
# 系统位数
SYSTEM_BIT: str = platform.architecture()[0]

# 清除控制台信息
_print_clear_dict: Dict = {
    'win32': 'cls',
    'linux': 'clear',
    'darwin': 'clear'
}
CONSOLE_CLEAR: str = _print_clear_dict[SYSTEM_NAME]
