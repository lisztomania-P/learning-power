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
from inside.Template.Meta_Singleton import SINGLETON

__all__ = []


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

    def Insert(self, pid: int) -> None:
        """
        Insert(pid: int) -> None
        插入专项答题id，如已存在则不进行操作

        :param pid: 专项答题id
        :return: None
        """
        if not self.Exist(pid=pid):
            sql = f'''INSERT INTO 
                {self.__name} (
                {self.__fields[1]}) 
                VALUES (?);'''
            data = (pid, )
            self.__cursor.execute(sql, data)
            self.__connect.commit()

    def Exist(self, pid: int) -> bool:
        """
        Exist(pid: int) -> bool
        是否存在指定id

        :param pid: 专项答题id
        :return: bool
        """
        sql = f'''SELECT 1 FROM {self.__name} 
                WHERE {self.__fields[1]}=?;'''
        data = (pid,)
        result = self.__cursor.execute(sql, data)
        try:
            next(result)
            return True
        except StopIteration:
            return False
