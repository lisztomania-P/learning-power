#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/23
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Get_Info.py
# @Function : 获取用户信息
from inside.Config.Api import API
from inside.Info.Task_Info import TASK_INFO
from inside.Info.User_Info import USER_INFO
from inside.Template.Meta_Singleton import SINGLETON
from inside.Tools.Requests import REQUESTS
__all__ = ['GET_INFO']


class GET_INFO(metaclass=SINGLETON):
    """获取信息类"""

    def __init__(self, token: str):
        """
        GET_INFO(token: str)
        初始化

        :param token: 令牌
        """
        self.__cookie = {'token': token}
        self.__info = USER_INFO()
        self._Init_Info()

    def _Init_Info(self) -> None:
        """
        _Init_Info() -> None
        初始化用户id

        :return: None
        """
        while True:
            try:
                html = REQUESTS().Get(
                    url=API().Aggregate_Score.geturl(),
                    cookies=self.__cookie
                )
                data = html.json()
                self.__info.User_Id = data['data']['userId']
                break
            except TypeError:
                continue

    def Get_Aggregate_Score(self) -> None:
        """
        Get_Aggregate_Score() -> None
        获取总积分

        :return: None
        """
        while True:
            try:
                html = REQUESTS().Get(
                    url=API().Aggregate_Score.geturl(),
                    cookies=self.__cookie
                )
                data = html.json()
                self.__info.Aggregate_Score = data['data']['score']
                break
            except TypeError:
                continue

    def Get_Level(self) -> None:
        """
        Get_Level() -> None
        获取等级

        :return: None
        """
        while True:
            try:
                html = REQUESTS().Get(
                    url=API().Level.geturl(),
                    cookies=self.__cookie
                )
                data = html.json()
                self.__info.Level = data['data']['level']
                self.__info.Level_Name = data['data']['levelName']
                self.__info.Rank_Accumulate_In_Country = \
                    data['data']['rankAccumulateInCountry']
                break
            except TypeError:
                continue

    def Get_Daily_Score(self) -> None:
        """
        Get_Daily_Score() -> None
        获取每日积分

        :return: None
        """
        while True:
            try:
                html = REQUESTS().Get(
                    url=API().Daily_Score.geturl(),
                    cookies=self.__cookie
                )
                data = html.json()
                self.__info.Daily_Score = data['data']['score']
                break
            except TypeError:
                continue

    def Get_Task_Bar(self) -> None:
        """
        Get_Task_Bar() -> None
        获取任务进度

        :return: None
        """
        while True:
            try:
                html = REQUESTS().Get(
                    url=API().Task_Bar.geturl(),
                    cookies=self.__cookie
                )
                data = html.json()
                for rule in data['data']['taskProgress']:
                    ruleId = rule['displayRuleId']
                    name = rule['title']
                    desc = rule['ruleDesc']
                    currentScore = rule['currentScore']
                    dayMaxScore = rule['dayMaxScore']
                    task = TASK_INFO(
                            ruleId=ruleId, name=name, desc=desc,
                            currentScore=currentScore, dayMaxScore=dayMaxScore
                        )
                    self.__info.Update_Task_Bar_Info(task_info=task)
                break
            except TypeError:
                continue
