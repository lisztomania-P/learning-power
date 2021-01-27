#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : DB_Config.py
# @Function : 数据库配置文件(此配置文件不可更改)
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['DB_CONFIG']


class DB_CONFIG(metaclass=SINGLETON):
    """
    数据库配置类
    """

    @property
    def User(self) -> str:
        """
        User -> str
        用户表名

        :return: str
        """
        return 'user'

    @property
    def User_Fields(self) -> tuple:
        """
        User_Fields -> tuple
        用户表字段

        :return: tuple
        """
        return 'ID', 'USERID', 'TOKEN', 'TIME'

    @property
    def User_Fields_Types(self) -> tuple:
        """
        User_Fields_Types -> tuple
        用户表字段类型

        :return: tuple
        """
        return 'INTEGER', 'INTEGER', 'TEXT', 'TEXT'

    @property
    def Task(self) -> str:
        """
        Task -> str
        任务表名

        :return: str
        """
        return 'task'

    @property
    def Task_Fields(self) -> tuple:
        """
        Task_Fields -> tuple
        任务表字段

        :return: tuple
        """
        return 'ID', 'LINK', 'ISREAD'

    @property
    def Task_Fields_Types(self) -> tuple:
        """
        Task_Fields_Types -> tuple
        任务表字段类型

        :return: tuple
        """
        return 'INTEGER', 'TEXT', 'INTEGER'

    @property
    def Article(self) -> str:
        """
        Article -> str
        文章表名

        :return: str
        """
        return 'article'

    @property
    def Article_Fields(self) -> tuple:
        """
        Article_Fields -> tuple
        文章表字段

        :return: tuple
        """
        return 'ID', 'ITEM', 'LINK', 'ISREAD'

    @property
    def Article_Fields_Types(self) -> tuple:
        """
        Article_Fields_Types -> tuple
        文章表字段类型

        :return: tuple
        """
        return 'INTEGER', 'TEXT', 'TEXT', 'INTEGER'

    @property
    def Video(self) -> str:
        """
        Video -> str
        视频表名

        :return: str
        """
        return 'video'

    @property
    def Video_Fields(self) -> tuple:
        """
        Video_Fields -> tuple
        视频表字段

        :return: tuple
        """
        return 'ID', 'ITEM', 'LINK', 'ISREAD'

    @property
    def Video_Fields_Types(self) -> tuple:
        """
        Video_Fields_Types -> tuple
        视频表字段类型

        :return: tuple
        """
        return 'INTEGER', 'TEXT', 'TEXT', 'INTEGER'
