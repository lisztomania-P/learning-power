#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : DB_Manage.py
# @Function : 数据库管理
import sqlite3
from inside.Config.Path import PATH
from inside.DB.DB_Article import DB_ARTICLE
from inside.DB.DB_Baidu_AI import DB_BAIDU_AI
from inside.DB.DB_Check import DB_CHECK
from inside.DB.DB_Project import DB_PROJECT
from inside.DB.DB_Task import DB_TASK
from inside.DB.DB_User import DB_USER
from inside.DB.DB_Video import DB_VIDEO
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['DB_MANAGE']


class DB_MANAGE(metaclass=SINGLETON):
    """数据库管理类"""

    def __init__(self):
        """
        DB_MANAGE()
        初始化时自动检查数据库信息

        """
        DB_CHECK().Check_Dir()
        self.__connect = sqlite3.connect(PATH().DB_File)
        self.__cursor = self.__connect.cursor()
        self.__Check_Table()

    def __Check_Table(self) -> None:
        """
        __Check_Table() -> None
        检查表

        :return: None
        """
        DB_CHECK().Check_Table(
            connect=self.__connect,
            cursor=self.__cursor
        )

    def Quit(self):
        self.__connect.close()

    @property
    def User(self) -> DB_USER:
        """
        User -> DB_USER
        用户表操作对象

        :return: DB_USER
        """
        return DB_USER(connect=self.__connect, cursor=self.__cursor)

    @property
    def Task(self) -> DB_TASK:
        """
        Task -> DB_TASK
        任务表操作对象

        :return: DB_TASK
        """
        return DB_TASK(connect=self.__connect, cursor=self.__cursor)

    @property
    def Article(self) -> DB_ARTICLE:
        """
        Article -> DB_ARTICLE
        文章表操作对象

        :return: DB_ARTICLE
        """
        return DB_ARTICLE(connect=self.__connect, cursor=self.__cursor)

    @property
    def Video(self) -> DB_VIDEO:
        """
        Video -> DB_VIDEO
        视频表操作对象

        :return: DB_VIDEO
        """
        return DB_VIDEO(connect=self.__connect, cursor=self.__cursor)

    @property
    def Project(self) -> DB_PROJECT:
        """
        Project -> DB_PROJECT
        专项答题表操作对象

        :return: DB_PROJECT
        """
        return DB_PROJECT(connect=self.__connect, cursor=self.__cursor)

    @property
    def Baidu_AI(self) -> DB_BAIDU_AI:
        """
        Baidu_AI -> DB_BAIDU_AI
        百度AI表操作对象

        @return: DB_BAIDU_AI
        """
        return DB_BAIDU_AI(connect=self.__connect, cursor=self.__cursor)
