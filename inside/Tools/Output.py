#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Output.py
# @Function : 信息输出
import os

from inside.Config.System import SYSTEM
from inside.Info.Info_Manage import INFO_MANAGE
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['OUTPUT', 'Info']


class OUTPUT(metaclass=SINGLETON):
    """
    输出信息
    """

    @classmethod
    def Info(cls):
        os.system(command=SYSTEM().Clear)
        temp = INFO_MANAGE()
        level = temp.Level_Info
        print(f"项目地址:https://github.com/lisztomania-Zero/learning-power")
        print(f"用户ID:{temp.Id}\n"
              f"等级:{level[0]}\t段位:{level[1]}\t全国排名:{level[2]}\n"
              f"总积分:{temp.Aggregate_Score}\t今日积分:{temp.Daily_Score}\n"
              f"每日积分细则:")
        print()
        for index, value in enumerate(list(temp.Task_Bar.values())):
            if (index+1) % 5 == 0:
                print(f"{value.Name}:{value.Current_Score}分")
                continue
            print(f"{value.Name}:{value.Current_Score}分\t", end='')
        print('\n')


_inst = OUTPUT()
Info = _inst.Info
