#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/7
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : check_task.py
# @Function : 检查任务
from selenium.common.exceptions import TimeoutException

from config.task_config import WRAP_CLASS_NAME
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


def check_wrap(task_driver: WebDriver) -> bool:
    try:
        wait: WebDriverWait = WebDriverWait(task_driver, 3)
        wrap_Ec = EC.presence_of_element_located(
            (
                By.CLASS_NAME, WRAP_CLASS_NAME
            )
        )
        wrap = wait.until(wrap_Ec)
        return True
    except TimeoutException:
        return False

