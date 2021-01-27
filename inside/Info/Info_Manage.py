#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/23
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Info_Manage.py
# @Function : 信息管理
from typing import Dict, Tuple

from inside.Info.Get_Info import GET_INFO
from inside.Info.Task_Info import TASK_INFO
from inside.Info.User_Info import USER_INFO
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['INFO_MANAGE']


class INFO_MANAGE(metaclass=SINGLETON):
    """信息管理类"""
    __Get: GET_INFO

    def __init__(self):
        """
        INFO_MANAGE()
        初始化

        """
        self.__self = '_'+type(self).__name__

    def Init(self, token: str) -> None:
        """
        Init(token: str) -> None
        初始化信息获取

        :param token: 令牌
        :return: None
        """
        self.__Get = GET_INFO(token=token)

    @property
    def Get(self) -> GET_INFO:
        """
        Get -> GET_INFO
        信息获取类

        :return: GET_INFO
        """
        if hasattr(self, self.__self+'__Get'):
            return self.__Get
        raise Exception(f"检测到更新信息类未初始化\n"
                        f"请先调用{type(self).__name__}().Init(token=xxx)")

    @property
    def Id(self) -> int:
        """
        Id - > int
        用户ID

        :return: int
        """
        return USER_INFO().User_Id

    @property
    def Aggregate_Score(self) -> float:
        """
        Aggregate_Score -> float
        总积分

        :return: float
        """
        self.Get.Get_Aggregate_Score()
        return USER_INFO().Aggregate_Score

    @property
    def Daily_Score(self) -> float:
        """
        Daily_Score -> float
        每日积分

        :return: float
        """
        self.Get.Get_Daily_Score()
        return USER_INFO().Daily_Score

    @property
    def Level_Info(self) -> Tuple[int, str, int]:
        """
        Level -> int
        等级、段位、全国排名

        :return: Tuple[int, str, int]
        """
        self.Get.Get_Level()
        return (USER_INFO().Level,
                USER_INFO().Level_Name,
                USER_INFO().Rank_Accumulate_In_Country)

    @property
    def Task_Bar(self) -> Dict[int, TASK_INFO]:
        """
        Task_Bar -> Dict[int, TASK_INFO]
        任务进度

        :return: Dict[int, TASK_INFO]
        """
        self.Get.Get_Task_Bar()
        return USER_INFO().Task_Bar
