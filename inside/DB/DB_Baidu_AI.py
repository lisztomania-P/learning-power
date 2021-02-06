#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/2/6
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : DB_Baidu_AI.py
# @Function : 百度AI操作类
from sqlite3 import Connection, Cursor

from inside.DB.DB_Config import DB_CONFIG
from inside.DB.Table_Class.Baidu_AI import BAIDU_AI
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['DB_BAIDU_AI']


class DB_BAIDU_AI(metaclass=SINGLETON):
    """百度AI表操作类"""

    def __init__(self, connect: Connection, cursor: Cursor):
        """
        初始化

        :param connect: 数据库连接对象
        :param cursor: 数据库光标
        """
        self.__connect = connect
        self.__cursor = cursor
        self.__name = DB_CONFIG().Baidu_AI
        self.__fields = DB_CONFIG().Baidu_AI_Fields

    def Insert(self, baidu_ai: BAIDU_AI) -> None:
        """
        Insert(article: ARTICLE) -> None
        插入百度AI，如表不为空则清空表

        @param baidu_ai: 百度AI
        @return: None
        """
        if not self.Empty():
            self.Delete()
        sql = f'''INSERT INTO
            {self.__name} (
            {self.__fields[1]}, 
            {self.__fields[2]}) 
            VALUES (?, ?);'''
        data = (
            baidu_ai.Ak,
            baidu_ai.Sk
        )
        self.__cursor.execute(sql, data)
        self.__connect.commit()

    def Seq_Init(self) -> None:
        """
        Seq_Init() -> None
        将百度AI表的数据序号重置为0

        @return: None
        """
        sql = f'''UPDATE sqlite_sequence SET seq=0 WHERE name='{self.__name}';'''
        self.__cursor.execute(sql)
        self.__connect.commit()

    def Delete(self) -> None:
        """
        Delete() -> None
        清空百度AI表，并重置序号

        @return: None
        """
        sql = f'''DELETE FROM {self.__name};'''
        self.__cursor.execute(sql)
        self.__connect.commit()
        self.Seq_Init()

    def Query(self) -> BAIDU_AI:
        """
        Query() -> BAIDU_AI
        获取百度AI

        @return: BAIDU_AI
        """
        sql = f'''SELECT * FROM {self.__name} LIMIT 1;'''
        result = self.__cursor.execute(sql)
        temp = next(result)
        return BAIDU_AI(ak=temp[1], sk=temp[2])

    def Empty(self) -> bool:
        """
        Empty() -> bool
        是否为空

        @return: bool
        """
        sql = f'''SELECT 1 FROM {self.__name} LIMIT 1;'''
        result = self.__cursor.execute(sql)
        try:
            next(result)
            return False
        except StopIteration:
            return True

    def Exist(self, baidu_ai: BAIDU_AI) -> bool:
        """
        Exist(baidu_ai: BAIDU_AI = None) -> bool
        是否存在指定百度AI

        @param baidu_ai: 百度AI
        @return:
        """
        sql = f'''SELECT 1 FROM {self.__name} 
                WHERE {self.__fields[1]}=? 
                AND {self.__fields[2]}=?;'''
        data = (
            baidu_ai.Ak,
            baidu_ai.Sk
        )
        result = self.__cursor.execute(sql, data)
        try:
            next(result)
            return True
        except StopIteration:
            return False
