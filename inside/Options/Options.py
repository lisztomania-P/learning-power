#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/16
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Options_Manage.py
# @Function : 选项
from typing import Dict

from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['OPTIONS']


class OPTIONS(metaclass=SINGLETON):
    """选项类"""

    def __init__(self):
        """
        OPTIONS()
        初始化，默认选项

        """
        self.__mute_audio = True
        self.__headless = True
        self.__token = True
        self.__baidu_ai = False
        self.__task_options = {
            1: ['文章', False],
            2: ['视频', False],
            3: ['每日答题', False],
            4: ['每周答题', False],
            5: ['专项答题', False]
        }

    @property
    def Mute_Audio(self) -> bool:
        """
        Mute_Audio -> bool
        获取禁音选项

        :return: bool
        """
        return self.__mute_audio

    @Mute_Audio.setter
    def Mute_Audio(self, on: bool) -> None:
        """
        Mute_Audio -> None
        设置禁音选项
            使用方法：Mute_Audio = True or False

        :param on: 开关
        :return: None
        """
        self.__mute_audio = on

    @property
    def Headless(self) -> bool:
        """
        Headless -> bool
        获取无窗口化选项

        :return: bool
        """
        return self.__headless

    @Headless.setter
    def Headless(self, on: bool) -> None:
        """
        Headless -> None
        设置无窗口化选项
            使用方法：Headless = True or False

        :param on: 开关
        :return: None
        """
        self.__headless = on

    @property
    def Token(self) -> bool:
        """
        Token -> bool
        获取持久化访问选项

        :return: bool
        """
        return self.__token

    @Token.setter
    def Token(self, on: bool) -> None:
        """
        Token -> None
        设置持久化访问选项
            使用方法：Token = True or False

        :param on: 开关
        :return: None
        """
        self.__token = on

    @property
    def Task_Options(self) -> Dict[int, str]:
        """
        Task_Options -> Dict[int, str]
        任务选项，不暴露是否选择情况

        :return: Dict[int, str]
        """
        temp = {}
        for key, value in self.__task_options.items():
            temp[key] = value[0]
        return temp

    def Task_Option_Set_On(self, seq: int) -> None:
        """
        Task_Option_Set_On(seq: int) -> None
        打开指定任务选项

        :param seq: 任务序号
        :return: None
        """
        self.__task_options[seq][-1] = True

    def Task_Option_Set_On_All(self) -> None:
        """
        Task_Option_Set_On_All() -> None
        任务选项全选

        :return: None
        """
        for key in self.__task_options.keys():
            self.__task_options[key][-1] = True

    def Task_Option_Set_Off_All(self) -> None:
        """
        Task_Option_Set_Off_All() -> None
        任务选项初始化

        :return: None
        """
        for key in self.__task_options.keys():
            self.__task_options[key][-1] = False

    @property
    def Article(self) -> bool:
        """
        Article -> bool
        文章选项

        :return: bool
        """
        return self.__task_options[1][-1]

    @property
    def Video(self) -> bool:
        """
        Video -> bool
        视频选项

        :return: bool
        """
        return self.__task_options[2][-1]

    @property
    def Daily_Answer(self) -> bool:
        """
        Daily_Answer -> bool
        每日答题选项

        :return: bool
        """
        return self.__task_options[3][-1]

    @property
    def Weekly_Answer(self) -> bool:
        """
        Weekly_Answer -> bool
        每周答题选项

        :return: bool
        """
        return self.__task_options[4][-1]

    @property
    def Project_Answer(self) -> bool:
        """
        Project_Answer -> bool
        专项答题选项

        :return: bool
        """
        return self.__task_options[5][-1]

    @property
    def Baidu_AI(self) -> bool:
        """
        Baidu_AI -> bool
        百度AI选项

        Returns: bool

        """
        return self.__baidu_ai

    @Baidu_AI.setter
    def Baidu_AI(self, on: bool) -> None:
        """
        Baidu_AI = on: bool
        设置百度AI选项

        Args:
            on: bool

        Returns: None

        """
        self.__baidu_ai = on
