#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/7
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : get_random.py
# @Function : 随机数获取
import random
import time


def get_random_int(a: int, b: int) -> int:
    random.seed(time.time())
    return random.randint(a=a, b=b)


def get_random_float(a: float, b: float) -> float:
    random.seed(time.time())
    return random.uniform(a=a, b=b)
