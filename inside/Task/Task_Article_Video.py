#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/25
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Task_Article_Video.py
# @Function : 文章视频任务
import time
from typing import Union

from tqdm import tqdm
from selenium.webdriver.chrome.webdriver import WebDriver

from inside.Config.Api import API
from inside.DB.Table_Class.Article import ARTICLE
from inside.DB.Table_Class.Video import VIDEO
from inside.Template.Meta_Singleton import SINGLETON
from inside.Tools.Network import NETWORK
from inside.Tools.Random import RANDOM

__all__ = ['TASK_ARTICLE_VIDEO']


class TASK_ARTICLE_VIDEO(metaclass=SINGLETON):

    def __init__(self, task_driver: WebDriver):
        """
        TASK_ARTICLE_VIDEO(task_driver: WebDriver)
        初始化

        :param task_driver: 驱动
        """
        self.__driver = task_driver
        self.__network = NETWORK()

    def __Check(self, item: str, tq: int) -> None:
        """
        __Check(item: str, tq: int) -> None
        监测任务的完成

        :param item: 任务编号
        :param tq: 等待程度
        :return: None
        """
        bar = tqdm(
            desc=item,
            total=tq,
            unit='it',
            leave=False,
            ncols=70
        )
        count = 0
        start = time.time()
        while True:
            js = "document.documentElement.scrollTop={speed}"
            self.__driver.execute_script(
                script=js.format(speed=RANDOM.Int(a=1, b=10))
            )
            temp = self.__network.Get()
            if API().Task_Check.geturl() in temp.keys() or \
                    time.time() - start >= 35:
                count += 1
                bar.update(n=1)
                start = time.time()
            if count >= tq:
                break
            time.sleep(0.1)
        bar.close()

    def Do(self, task: Union[ARTICLE, VIDEO], tq: int) -> None:
        """
        Do(task: Union[ARTICLE, VIDEO]) -> None
        进行一次文章或视频任务

        :param task: 任务
        :param tq: 等待程度
        :return: None
        """
        self.__network.Clear()
        self.__driver.get(task.Link)
        self.__Check(item=task.Item, tq=tq)
