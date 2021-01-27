#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : DB_User.py
# @Function : 用户表操作
from sqlite3 import Connection, Cursor

from inside.DB.DB_Config import DB_CONFIG
from inside.DB.Table_Class.User import USER
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['DB_USER']


class DB_USER(metaclass=SINGLETON):
    """用户表操作类"""

    def __init__(self, connect: Connection, cursor: Cursor):
        """
        初始化

        :param connect: 数据库连接对象
        :param cursor: 数据库光标
        """
        self.__connect = connect
        self.__cursor = cursor
        self.__name = DB_CONFIG().User
        self.__fields = DB_CONFIG().User_Fields

    def Insert(self, user: USER) -> None:
        """
        Insert(user: USER) -> None
        插入用户，插入之前如果存在用户则清空用户表，以保证只有一个用户使用

        :param user: 用户
        :return: None
        """
        if self.Exist():
            self.Delete()
        sql = f'''INSERT INTO 
            {self.__name} 
            ({self.__fields[1]}, 
            {self.__fields[2]}, 
            {self.__fields[3]})
            VALUES(?, ?, ?);'''
        data = (
            user.Id,
            user.Token,
            user.Time
        )
        self.__cursor.execute(sql, data)
        self.__connect.commit()

    def Seq_Init(self) -> None:
        """
        Seq_Init() -> None
        将用户表的数据序号重置为0

        :return: None
        """
        sql = f'''UPDATE sqlite_sequence SET seq=0 WHERE name='{self.__name}';'''
        self.__cursor.execute(sql)
        self.__connect.commit()

    def Delete(self) -> None:
        """
        Delete() -> None
        清空用户表，并重置序号

        :return: None
        """
        sql = f'''DELETE FROM {self.__name};'''
        self.__cursor.execute(sql)
        self.__connect.commit()
        self.Seq_Init()

    def Update(self, user: USER) -> None:
        """
        Update(user: USER) -> None
        更新指定用户token

        :param user: 用户
        :return: None
        """
        sql = f'''UPDATE {self.__name} 
            SET {self.__fields[2]}=? 
            WHERE {self.__fields[1]} =?;'''
        data = (
            user.Token,
            user.Id
        )
        self.__cursor.execute(sql, data)
        self.__connect.commit()

    def Query(self) -> USER:
        """
        Query() -> USER
        获取一条用户

        :return: USER
        """
        sql = f'''SELECT * FROM {self.__name} LIMIT 1;'''
        result = self.__cursor.execute(sql)
        temp = next(result)
        user = USER(
            user_id=temp[1],
            token=temp[2]
        )
        return user

    def Exist(self) -> bool:
        """
        Exist() -> bool
        是否存在用户

        :return: bool
        """
        sql = f'''SELECT 1 FROM {self.__name} LIMIT 1;'''
        result = self.__cursor.execute(sql)
        try:
            next(result)
            return True
        except StopIteration:
            return False

    def Exist_User(self, user: USER) -> bool:
        """
        Exist(user: USER) -> bool
        是否存在指定用户

        :return: bool
        """
        sql = f'''SELECT 1 FROM {self.__name} 
            WHERE {self.__fields[1]}=? LIMIT 1;'''
        data = (user.Id, )
        result = self.__cursor.execute(sql, data)
        try:
            next(result)
            return True
        except StopIteration:
            return False
