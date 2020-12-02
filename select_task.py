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
    explain = '''请选择任务:
    1、{}    2、{}
    选择:'''.format(TASK_OPTIONS[1][0], TASK_OPTIONS[2][0])
    args = input(explain)
    return args


def Select_task():
    while True:
        try:
            arg = __select_task()
            option = [int(x) for x in arg.split(' ')]
            for op in option:
                TASK_OPTIONS[op][1] = True
            break
        except:
            for key in TASK_OPTIONS.keys():
                TASK_OPTIONS[key][1] = False
            continue
