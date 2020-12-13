#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/11/28
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : main.py
# @Function : 入口

from init import init_driver
from login.login import Login
from init.select_task import Select_task
from task.task_manage import Task_Manage

driver = init_driver.Driver()
login = Login(driver=driver)
# 登录
login.login()
task_manage = Task_Manage(driver=driver)
# 选择任务
while True:
    if Select_task():
        task_manage.start()
    else:
        driver.quit()
        break
