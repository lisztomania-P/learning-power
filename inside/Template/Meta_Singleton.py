#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/14
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Meta_Singleton.py
# @Function : 单例基类
from abc import ABCMeta

__all__ = ['SINGLETON', 'SINGLETON_ABC']


class SINGLETON(type):
    """单例元类"""
    __instances = {}

    def __call__(cls, *args, **kwargs):
        """
        重载()，确保返回的为唯一对象

        :param args:
        :param kwargs:
        :return:
        """
        if not cls.__instances.get(cls):
            cls.__instances[cls] = super(SINGLETON, cls).__call__(*args,
                                                                  **kwargs)
        return cls.__instances[cls]


class SINGLETON_ABC(ABCMeta):
    """抽象类的单例元类"""
    __instances = {}

    def __call__(cls, *args, **kwargs):
        """
        重载()，确保返回的为唯一对象

        :param args:
        :param kwargs:
        :return:
        """
        if not cls.__instances.get(cls):
            cls.__instances[cls] = super(SINGLETON_ABC, cls).__call__(*args,
                                                                      **kwargs)
        return cls.__instances[cls]
