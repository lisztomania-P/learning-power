#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/11/28
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : daily_article.py
# @Function : 任务id:1 and 1002

import time
import random
import out_msg
from typing import Tuple
from selenium.webdriver.chrome.webdriver import WebDriver
from configuration import PAGE_ROLL_JS, MIX_ARG, ARTICLE_TIME


class Daily_Article(object):
    __success: bool = False
    __page_roll_js: str = PAGE_ROLL_JS
    __article_time: Tuple = ARTICLE_TIME

    def __init__(self):
        random.seed(a=MIX_ARG)

    @out_msg.out_print
    def do(self, task_driver: WebDriver, task_url: str):
        task_driver.get(url=task_url)
        for i in range(1, random.randint(
                           self.__article_time[0], self.__article_time[1]
                       )):
            mix: float = random.uniform(0, 10)
            js: str = self.__page_roll_js.format(i*10+mix)
            task_driver.execute_script(script=js)
            time.sleep(1)
        self.__success = True

    def is_success(self) -> bool:
        return self.__success
