#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/2/4
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : DB_Project.py
# @Function : 专项答题表操作
from sqlite3 import Connection, Cursor

from inside.DB.DB_Config import DB_CONFIG
from inside.DB.Table_Class.Project import PROJECT
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['DB_PROJECT']


class DB_PROJECT(metaclass=SINGLETON):
    """专项答题表操作类"""

    def __init__(self, connect: Connection, cursor: Cursor):
        """
        初始化

        :param connect: 数据库连接对象
        :param cursor: 数据库光标
        """
        self.__connect = connect
        self.__cursor = cursor
        self.__name = DB_CONFIG().Project
        self.__fields = DB_CONFIG().Project_Fields

    def Insert(self, project: PROJECT) -> None:
        """
        Insert(project: PROJECT) -> None
        插入专项答题id，如已存在则不进行操作

        :param project: 专项答题
        :return: None
        """
        if not self.Exist(project=project):
            sql = f'''INSERT INTO 
                {self.__name} (
                {self.__fields[1]}) 
                VALUES (?);'''
            data = (project.Id, )
            self.__cursor.execute(sql, data)
            self.__connect.commit()

    def Exist(self, project: PROJECT) -> bool:
        """
        Exist(project: PROJECT) -> bool
        是否存在指定id

        :param project: 专项答题
        :return: bool
        """
        sql = f'''SELECT 1 FROM {self.__name} 
                WHERE {self.__fields[1]}=?;'''
        data = (project.Id,)
        result = self.__cursor.execute(sql, data)
        try:
            next(result)
            return True
        except StopIteration:
            return False
