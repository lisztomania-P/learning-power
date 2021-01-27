#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/22
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : User_Info.py
# @Function : 用户信息
from typing import Dict

from inside.Info.Task_Info import TASK_INFO
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['USER_INFO']


class USER_INFO(metaclass=SINGLETON):
    """用户信息类"""
    __token: str
    __user_id: int
    __aggregate_score: float
    __daily_score: float
    __level: int
    __level_name: str
    __rank_accumulate_in_country: int

    __task_bar: Dict[int, TASK_INFO]

    def __init__(self):
        """
        USER_INFO()
        初始化

        """
        self.__self = '_'+type(self).__name__

    @property
    def User_Id(self) -> int:
        """
        User_Id -> int
        用户ID

        :return: int
        """
        if hasattr(self, self.__self+'__user_id'):
            return self.__user_id
        return -1

    @User_Id.setter
    def User_Id(self, user_id: int) -> None:
        """
        User_Id -> None
        设置用户ID

        :param user_id: ID
        :return: None
        """
        if not hasattr(self, self.__self+'__user_id'):
            self.__user_id = user_id

    @property
    def Aggregate_Score(self) -> float:
        """
        Aggregate_Score -> float
        总积分

        :return: float
        """
        if hasattr(self, self.__self+'__aggregate_score'):
            return self.__aggregate_score
        return -1

    @Aggregate_Score.setter
    def Aggregate_Score(self, aggregate_score: float) -> None:
        """
        Aggregate_Score -> None
        设置总积分

        :param aggregate_score: 总积分
        :return: None
        """
        self.__aggregate_score = aggregate_score

    @property
    def Daily_Score(self) -> float:
        """
        Daily_Score -> float
        每日积分

        :return: float
        """
        if hasattr(self, self.__self+'__daily_score'):
            return self.__daily_score
        return -1

    @Daily_Score.setter
    def Daily_Score(self, daily_score: float) -> None:
        """
        Daily_Score -> None
        设置每日积分

        :param daily_score: 每日积分
        :return: None
        """
        self.__daily_score = daily_score

    @property
    def Level(self) -> int:
        """
        Level -> int
        等级

        :return: int
        """
        if hasattr(self, self.__self+'__level'):
            return self.__level
        return -1

    @Level.setter
    def Level(self, level: int) -> None:
        """
        Level -> None
        设置等级

        :param level: 等级
        :return: None
        """
        self.__level = level

    @property
    def Level_Name(self) -> str:
        """
        Level_Name -> str
        段位

        :return: str
        """
        if hasattr(self, self.__self+'__level_name'):
            return self.__level_name
        return ''

    @Level_Name.setter
    def Level_Name(self, level_name: str) -> None:
        """
        Level_Name -> None
        设置段位

        :param level_name: 段位
        :return: None
        """
        self.__level_name = level_name

    @property
    def Rank_Accumulate_In_Country(self) -> int:
        """
        Rank_Accumulate_In_Country -> int
        全国排名

        :return: int
        """
        if hasattr(self, self.__self+'__rank_accumulate_in_country'):
            return self.__rank_accumulate_in_country
        return -1

    @Rank_Accumulate_In_Country.setter
    def Rank_Accumulate_In_Country(self, rank_accumulate_in_country: int) -> None:
        """
        Rank_Accumulate_In_Country -> None
        设置全国排名

        :param rank_accumulate_in_country: 全国排名
        :return: None
        """
        self.__rank_accumulate_in_country = rank_accumulate_in_country

    @property
    def Task_Bar(self) -> Dict[int, TASK_INFO]:
        """
        Task_Bar -> Dict[int, TASK_INFO]
        任务进度

        :return: Dict[int, TASK_INFO]
        """
        if hasattr(self, self.__self+'__task_bar'):
            return self.__task_bar
        else:
            return {}

    def Update_Task_Bar_Info(self, task_info: TASK_INFO) -> None:
        """
        Update_Task_Bar_Info(task_info: TASK_INFO) -> None
        更新任务进度

        :param task_info: 任务类
        :return: None
        """
        if not hasattr(self, self.__self+'__task_bar'):
            self.__task_bar = {task_info.Rule_Id: task_info}
        else:
            self.__task_bar[task_info.Rule_Id] = task_info
