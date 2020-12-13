#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/11/28
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : daily_article.py
# @Function : 任务id:1 and 1002

import time
from tqdm import tqdm
from task import check_task
from tools import get_random
from config import out_msg
from selenium.webdriver.chrome.webdriver import WebDriver
from config.task_config import PAGE_ROLL_JS, TASK_ID, TASK_IDE
from config.can_change_config import BAR_LENGTH


class Daily_Article(object):
    __success: bool = False

    def __init__(self):
        pass

    @out_msg.out_print
    def do(self, task_driver: WebDriver, task_url: str, timeout: int):
        task_driver.get(url=task_url)
        if check_task.check_wrap(task_driver=task_driver):
            return None
        bar = tqdm(
            desc=TASK_IDE[TASK_ID[1]],
            total=timeout,
            leave=False,
            ncols=BAR_LENGTH
        )
        for i in range(1, timeout+1):
            bar.update(1)
            mix: float = get_random.get_random_float(
                a=0,
                b=10
            )
            js: str = PAGE_ROLL_JS.format(i*10+mix)
            task_driver.execute_script(script=js)
            time.sleep(1)
        bar.close()
        self.__success = True

    def is_success(self) -> bool:
        return self.__success
