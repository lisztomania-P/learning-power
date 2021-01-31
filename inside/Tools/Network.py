#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/20
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Network.py
# @Function : 网络日志
import json
import psutil
import gc
from _queue import Empty
from queue import Queue
from threading import Thread
from typing import Dict

from selenium.webdriver.chrome.webdriver import WebDriver

__all__ = ['NETWORK']

from inside.Template.Meta_Singleton import SINGLETON


class NETWORK(metaclass=SINGLETON):
    """network日志类，实现原理为队列+线程"""

    __task: Thread
    __driver: WebDriver

    def __init__(self):
        """
        NETWORK()
        初始化，队列

        """
        self.__self = '_'+type(self).__name__
        self.__queue = Queue(maxsize=0)
        self.__on = True

    def Init(self, driver: WebDriver):
        if not hasattr(self, self.__self+'__driver'):
            self.__driver = driver
            self.__task = Thread(target=self.__Get_Log)
            self.__task.start()
        else:
            print('已初始化')

    def __Get_Log(self) -> None:
        """
        __Get_Log() -> None
        获取有效日志，并加入队列，结束条件为开关

        :return: None
        """
        while True:
            if not self.__on:
                break
            logs = self.__driver.get_log(log_type='performance')
            for log in logs:
                log['message'] = json.loads(log['message'])
                try:
                    url = log['message']['message']['params']['request']['url']
                    requestId = log['message']['message']['params']['requestId']
                    while psutil.virtual_memory().used / psutil.virtual_memory().total >= 0.95:
                        gc.collect()
                        continue
                    self.__queue.put({url: requestId})
                except KeyError:
                    continue

    def __On_Logs(self) -> None:
        """
        __On_Logs() -> None
        开启日志
        :return: None
        """
        if not self.__task.is_alive():
            self.__task = Thread(target=self.__Get_Log)
            self.__task.start()

    def Get(self) -> Dict:
        """
        Get() -> Dict
        获取日志

        :return:Dict
            格式为{url: requestId}
        """
        try:
            return self.__queue.get_nowait()
        except Empty:
            return {}

    def GetResponseBody(self, requestId: str) -> Dict:
        """
        GetResponseBody(requestId: str) -> Dict
        获取指定请求Id的响应信息，考虑到网络延迟，可能会触发WebDriverException错误，
            建议使用try/except对同一requestId进行循环获取

        :param requestId: str
        :return: Dict
            格式为：{'base64Encoded': bool, 'body': str}
        """
        body = self.__driver.execute_cdp_cmd(
            cmd='Network.getResponseBody',
            cmd_args={'requestId': requestId}
        )
        return body

    def Clear(self) -> None:
        """
        Clear() -> None
        清空缓存日志

        :return: None
        """
        self.__queue.queue.clear()

    @property
    def On(self) -> bool:
        """
        On -> bool
        查看开关

        :return: bool
        """
        return self.__on

    @On.setter
    def On(self, on: bool) -> None:
        """
        On -> bool
        设置开关

        :param on: bool
        :return: None
        """
        self.__on = on
        if self.__on:
            self.__On_Logs()

    @property
    def Is_Alive(self) -> bool:
        """
        Is_Alive -> bool
        线程是否存活

        :return: bool
        """
        if hasattr(self, self.__self+'__task'):
            return self.__task.is_alive()
        return False

    def Quit(self) -> None:
        """
        Quit() -> None
        退出

        :return: None
        """
        self.__on = False
