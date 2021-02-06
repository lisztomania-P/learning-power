#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : DB_Create.py
# @Function : 数据库表创建
from sqlite3 import Connection, Cursor

from inside.DB.DB_Config import DB_CONFIG
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['DB_CREATE']


class DB_CREATE(metaclass=SINGLETON):
    """数据库表创建操作类"""

    def __init__(self, connect: Connection, cursor: Cursor):
        """
        DB_CREATE(connect: Connection, cursor: Cursor)
        初始化

        :param connect: 数据库连接对象
        :param cursor: 光标
        """
        self.__connect = connect
        self.__cursor = cursor

    def User(self) -> None:
        """
        User() -> None
        用户表创建

        :return: None
        """
        name = DB_CONFIG().User
        fields = DB_CONFIG().User_Fields
        fields_types = DB_CONFIG().User_Fields_Types
        sql = f'''CREATE TABLE {name}
        ({fields[0]} {fields_types[0]} PRIMARY KEY AUTOINCREMENT,
        {fields[1]} {fields_types[1]} NOT NULL,
        {fields[2]} {fields_types[2]} NOT NULL,
        {fields[3]} {fields_types[3]} NOT NULL
        );'''
        self.__cursor.execute(sql)
        self.__connect.commit()

    def Task(self) -> None:
        """
        Task() -> None
        任务表创建

        :return: None
        """
        name = DB_CONFIG().Task
        fields = DB_CONFIG().Task_Fields
        fields_types = DB_CONFIG().Task_Fields_Types
        sql = f'''CREATE TABLE {name}
        ({fields[0]} {fields_types[0]} PRIMARY KEY AUTOINCREMENT,
        {fields[1]} {fields_types[1]} NOT NULL,
        {fields[2]} {fields_types[2]} NOT NULL
        );'''
        self.__cursor.execute(sql)
        self.__connect.commit()

    def Article(self) -> None:
        """
        Article() -> None
        文章表创建

        :return: None
        """
        name = DB_CONFIG().Article
        fields = DB_CONFIG().Article_Fields
        fields_types = DB_CONFIG().Article_Fields_Types
        sql = f'''CREATE TABLE {name}
        ({fields[0]} {fields_types[0]} PRIMARY KEY AUTOINCREMENT,
        {fields[1]} {fields_types[1]} NOT NULL,
        {fields[2]} {fields_types[2]} NOT NULL,
        {fields[3]} {fields_types[3]} NOT NULL
        );'''
        self.__cursor.execute(sql)
        self.__connect.commit()

    def Video(self) -> None:
        """
        Video() -> None
        视频表创建

        :return: None
        """
        name = DB_CONFIG().Video
        fields = DB_CONFIG().Video_Fields
        fields_types = DB_CONFIG().Video_Fields_Types
        sql = f'''CREATE TABLE {name}
        ({fields[0]} {fields_types[0]} PRIMARY KEY AUTOINCREMENT,
        {fields[1]} {fields_types[1]} NOT NULL,
        {fields[2]} {fields_types[2]} NOT NULL,
        {fields[3]} {fields_types[3]} NOT NULL
        );'''
        self.__cursor.execute(sql)
        self.__connect.commit()

    def Project(self) -> None:
        """
        Project() -> None
        专项答题表创建

        :return: None
        """
        name = DB_CONFIG().Project
        fields = DB_CONFIG().Project_Fields
        fields_types = DB_CONFIG().Project_Fields_Types
        sql = f'''CREATE TABLE {name}
        ({fields[0]} {fields_types[0]} PRIMARY KEY AUTOINCREMENT,
        {fields[1]} {fields_types[1]} NOT NULL
        );'''
        self.__cursor.execute(sql)
        self.__connect.commit()

    def Baidu_AI(self) -> None:
        """
        Baidu_AI() -> None
        百度AI表创建

        :return: None
        """
        name = DB_CONFIG().Baidu_AI
        fields = DB_CONFIG().Baidu_AI_Fields
        fields_types = DB_CONFIG().Baidu_AI_Fields_Types
        sql = f'''CREATE TABLE {name}
        ({fields[0]} {fields_types[0]} PRIMARY KEY AUTOINCREMENT,
        {fields[1]} {fields_types[1]} NOT NULL,
        {fields[2]} {fields_types[2]} NOT NULL
        );'''
        self.__cursor.execute(sql)
        self.__connect.commit()