#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/11/16
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : Thread.py
# @Function : 可停止的线程
import threading


class THREAD(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(THREAD, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()
        self.__target = kwargs.get('target')
        self.__args = kwargs.get('args')

    def run(self) -> None:
        while self.__running.isSet():
            self.__flag.wait()
            if self.__args:
                self.__target(*self.__args)
            else:
                self.__target()

    def pause(self):
        self.__flag.clear()

    def resume(self):
        self.__flag.set()

    def stop(self):
        self.__flag.set()
        self.__running.clear()
