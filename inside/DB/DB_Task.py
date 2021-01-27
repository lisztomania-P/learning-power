#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : DB_Task.py
# @Function : 任务表操作
from sqlite3 import Connection, Cursor

from inside.DB.DB_Config import DB_CONFIG
from inside.DB.Table_Class.Task import TASK
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['DB_TASK']


class DB_TASK(metaclass=SINGLETON):
    """任务表操作类"""

    def __init__(self, connect: Connection, cursor: Cursor):
        """
        初始化

        :param connect: 数据库连接对象
        :param cursor: 光标
        """
        self.__connect = connect
        self.__cursor = cursor
        self.__name = DB_CONFIG().Task
        self.__fields = DB_CONFIG().Task_Fields

    def Insert(self, task: TASK) -> None:
        """
        Insert(task: TASK) -> None
        插入任务， 如任务已存在则不进行操作

        :param task: 任务
        :return: None
        """
        if not self.Exist(task=task):
            sql = f'''INSERT INTO
                {self.__name} (
                {self.__fields[1]}, 
                {self.__fields[2]})
                VALUES (?, ?);'''
            data = (
                task.Link,
                task.Is_Read_DB
            )
            self.__cursor.execute(sql, data)
            self.__connect.commit()

    def Update(self, task: TASK) -> None:
        """
        Update(task: TASK) -> None
        更新任务为已读， 如任务不存在则不进行操作

        :param task: 任务
        :return: None
        """
        if self.Exist(task=task):
            sql = f'''UPDATE {self.__name}
                SET {self.__fields[2]}=1
                WHERE {self.__fields[1]}=?'''
            data = (task.Link, )
            self.__cursor.execute(sql, data)
            self.__connect.commit()

    def Query(self) -> TASK:
        """
        Query() -> TASK
        随机获取一条未读任务

        :return: TASK
        """
        sql = f'''SELECT * FROM {self.__name} 
            WHERE {self.__fields[2]}=0 ORDER BY RANDOM() LIMIT 1;'''
        result = self.__cursor.execute(sql)
        temp = next(result)
        task = TASK(
            link=temp[1],
            isread=temp[2]
        )
        return task

    def Exist_Enough(self) -> bool:
        """
        Exist_Enough() -> bool
        是否存在未读任务

        :return: bool
        """
        sql = f'''SELECT 1 FROM {self.__name} 
            WHERE {self.__fields[2]}=0 LIMIT 1;'''
        result = self.__cursor.execute(sql)
        try:
            next(result)
            return True
        except StopIteration:
            return False

    def Empty(self) -> bool:
        """
        Empty() -> bool
        任务表是否为空

        :return: bool
        """
        sql = f'''SELECT 1 FROM {self.__name} LIMIT 1;'''
        result = self.__cursor.execute(sql)
        try:
            next(result)
            return False
        except StopIteration:
            return True

    def Exist(self, task: TASK) -> bool:
        """
        Exist(task: TASK) -> bool
        是否存在指定的任务

        :param task: 任务
        :return: bool
        """
        sql = f'''SELECT 1 FROM {self.__name}
            WHERE {self.__fields[1]} =?;'''
        data = (task.Link, )
        result = self.__cursor.execute(sql, data)
        try:
            next(result)
            return True
        except StopIteration:
            return False
