#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/23
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Task_Info.py
# @Function : 任务信息类
__all__ = ['TASK_INFO']


class TASK_INFO(object):
    """任务信息类"""

    def __init__(self, ruleId: int, name: str, desc: str, currentScore: int,
                 dayMaxScore: int):
        """
        TASK_INFO(ruleId: int, name: str, desc: str, currentScore: int,
                 dayMaxScore: int)
        初始化

        :param ruleId: ID
        :param name: 名称
        :param desc: 说明
        :param currentScore: 已获积分
        :param dayMaxScore: 最大积分
        """
        self.__rule_id = ruleId
        self.__name = name
        self.__desc = desc
        self.__current_score = currentScore
        self.__day_max_score = dayMaxScore

    @property
    def Rule_Id(self) -> int:
        """
        Rule_Id -> int
        Id

        :return: int
        """
        return self.__rule_id

    @property
    def Name(self) -> str:
        """
        Name -> str
        名称

        :return: str
        """
        return self.__name

    @property
    def Desc(self) -> str:
        """
        Desc -> str
        说明

        :return: str
        """
        return self.__desc

    @property
    def Current_Score(self) -> int:
        """
        Current_Score -> int
        已获积分

        :return: int
        """
        return self.__current_score

    @Current_Score.setter
    def Current_Score(self, currentScore: int) -> None:
        """
        Current_Score -> None
        设置已获积分

        :param currentScore: 更新积分
        :return: None
        """
        self.__current_score = currentScore

    @property
    def Day_Max_Score(self) -> int:
        """
        Day_Max_Score -> int
        最大积分

        :return: int
        """
        return self.__day_max_score

    @property
    def Difference_Score(self) -> int:
        """
        Difference_Score -> int
        剩余可获积分

        :return: int
        """
        return self.Day_Max_Score - self.Current_Score
