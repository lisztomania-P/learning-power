#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/1
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : select_task.py
# @Function : 选择任务

import out_msg
from configuration import TASK_OPTIONS


@out_msg.out_print
def __select_task() -> str:
    explain = "请选择任务:\n"
    for key, value in TASK_OPTIONS.items():
        explain += str(key) + '、' + value[0] + '\t'
    explain += "\n选择(选项请使用空格隔开，退出输入0):"
    args = input(explain).strip()
    return args


def __clear_options():
    for key in TASK_OPTIONS.keys():
        TASK_OPTIONS[key][1] = False


def Select_task() -> bool:
    while True:
        try:
            __clear_options()
            arg = __select_task()
            option = [int(x) for x in arg.split(' ')]
            if 0 in option:
                return False
            for op in option:
                TASK_OPTIONS[op][1] = True
            return True
        except (KeyError, ValueError):
            __clear_options()
            continue
