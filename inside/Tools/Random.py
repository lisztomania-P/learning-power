#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Random.py
# @Function : 随机数
import random
import time
from typing import Union

from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['RANDOM', 'Int', 'Float']


class RANDOM(metaclass=SINGLETON):
    """
    提供随机数
    """
    random.seed(time.time())

    @classmethod
    def Int(cls, a: int, b: int) -> int:
        """
        Int(a: int, b: int) -> int
        类方法
        输出随机整数，a<=结果<=b

        :param a: 起始数
        :param b: 结束数
        :return: int
        """
        return random.randint(a=a, b=b)

    # 浮点数
    @classmethod
    def Float(cls, a: Union[float, int], b: Union[float, int]) -> float:
        """
        Float(a: float, b: float) -> float
        类方法
        输出随机浮点数，a<=结果<=b

        :param a: 起始数
        :param b: 结束数
        :return: float
        """
        return random.uniform(a=a, b=b)

    @classmethod
    def Float_Precision(cls, a: Union[float, int], b: Union[float, int],
                        precision: int):
        return round(number=cls.Float(a=a, b=b), ndigits=precision)


_inst = RANDOM()
Int = _inst.Int
Float = _inst.Float
Float_Precision = _inst.Float_Precision
