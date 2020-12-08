#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/11/28
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : daily_article.py
# @Function : 任务id:1 and 1002

import time

import check_task
import get_random
import out_msg
from selenium.webdriver.chrome.webdriver import WebDriver
from configuration import PAGE_ROLL_JS


class Daily_Article(object):
    __success: bool = False
    __page_roll_js: str = PAGE_ROLL_JS

    def __init__(self):
        pass

    @out_msg.out_print
    def do(self, task_driver: WebDriver, task_url: str, timeout: int):
        task_driver.get(url=task_url)
        if check_task.check_wrap(task_driver=task_driver):
            return None
        for i in range(1, timeout):
            mix: float = get_random.get_random_float(
                a=0,
                b=10
            )
            js: str = self.__page_roll_js.format(i*10+mix)
            task_driver.execute_script(script=js)
            time.sleep(1)
        self.__success = True

    def is_success(self) -> bool:
        return self.__success
