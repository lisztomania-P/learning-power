#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/20
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : main.py
# @Function : 入口
import os

from inside.Config.System import SYSTEM
from inside.Driver.Driver_Manage import DRIVER_MANAGE
from inside.Login.Login import LOGIN
from inside.Options.Options_Manage import OPTIONS_MANAGE
from inside.Task.Mitmdump.Mitmdump import MITMDUMP
from inside.Task.Task_Manage import TASK_MANAGE
from inside.Tools.Network import NETWORK
from inside.Tools.Output import OUTPUT

if __name__ == '__main__':
    SYSTEM().Check_Chrome()
    os.system(command=SYSTEM().Clear)
    OPTIONS_MANAGE.Init_Options()
    MITMDUMP().Open()
    driver = DRIVER_MANAGE()
    network = NETWORK()
    network.Init(driver=driver.Task)
    if LOGIN(task_driver=driver.Task).Login():
        while True:
            OUTPUT.Info()
            OPTIONS_MANAGE.Task_Options()
            task = TASK_MANAGE(driver=driver.Task)
            task.Task()

