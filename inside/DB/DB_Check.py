#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : DB_Check.py
# @Function : 数据库检测
import os
import time
from sqlite3 import Cursor, Connection

from inside.Config.Path import PATH
from inside.DB.DB_Create import DB_CREATE
from inside.DB.DB_Config import DB_CONFIG
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['DB_CHECK']


class DB_CHECK(metaclass=SINGLETON):
    """数据库检测类"""

    @property
    def Dir(self) -> bool:
        """
        Dir -> bool
        是否存在数据库目录

        :return: bool
        """
        return os.path.exists(PATH().DB)

    def Check_Dir(self) -> None:
        """
        Check_Dir() -> None
        检查数据库目录是否存在，如不存在则自动创建

        :return: None
        """
        if not self.Dir:
            print(f"检测到数据库目录未创建\n"
                  f"自动创建中")
            os.mkdir(PATH().DB)
            print(f"数据库目录为{PATH().DB}")

    def _Exist_Table(self, cursor: Cursor, table_name: str) -> bool:
        """
        _Exist_Table(cursor: Cursor, table_name: str) -> None
        检查表是否存在

        :param cursor: 光标
        :param table_name: 表名
        :return: bool
        """
        sql = '''SELECT name FROM sqlite_master 
                WHERE type='table' 
                AND name=? COLLATE NOCASE;'''
        data = (table_name,)
        result = cursor.execute(sql, data)
        try:
            next(result)
            return True
        except StopIteration:
            return False

    def _Change_Table(self, connect: Connection, cursor: Cursor,
                      table_name: str) -> None:
        """
        _Change_Table(connect: Connection, cursor: Cursor,
                    table_name: str) -> None
        更改表名，在表名后面加上当前时间戳

        :param connect: 数据库连接对象
        :param cursor: 光标
        :param table_name: 表名
        :return: None
        """
        new_name = table_name + str(int(time.time()))
        sql = f'''ALTER TABLE {table_name} RENAME TO {new_name};'''
        print(f"检测到同名不同结构表<{table_name}>\n"
              f"自动为其重命名中")
        cursor.execute(sql)
        connect.commit()
        print(f"重命名为<{new_name}>")

    def _Check_Table_Fields(self, cursor: Cursor, table_name: str,
                            table_info: tuple) -> bool:
        """
        _Check_Table_Fields(cursor: Cursor, table_name: str,
                            table_info: tuple) -> bool
        检查表结构是否一致

        :param cursor: 光标
        :param table_name: 表名
        :param table_info: 表结构(从左至右顺序)
        :return: bool
        """
        sql = f'''PRAGMA TABLE_INFO({table_name})'''
        result = cursor.execute(sql)
        temp_name, temp_type = [], []
        for temp in result:
            temp_name.append(temp[1])
            temp_type.append(temp[2])
        return (tuple(temp_name), tuple(temp_type)) == table_info

    def _Check_Table(self, connect: Connection, cursor: Cursor,
                     table_name: str, table_info: tuple) -> bool:
        """
        _Check_Table(connect: Connection, cursor: Cursor,
                    table_name: str, table_info: tuple) -> bool:
        检查表是否存在，且表结构是否一致；如存在且表结构不一致，则将已存在同名表重命名，返回False

        :param connect: 数据库连接对象
        :param cursor: 光标
        :param table_name: 表名
        :param table_info: 表结构(从左至右顺序)
        :return: bool
        """
        if self._Exist_Table(cursor=cursor, table_name=table_name):
            temp = self._Check_Table_Fields(cursor=cursor,
                                            table_name=table_name,
                                            table_info=table_info)
            if temp:
                return temp
            else:
                self._Change_Table(connect=connect, cursor=cursor,
                                   table_name=table_name)
        return False

    def Check_User(self, connect: Connection, db_create: DB_CREATE,
                   cursor: Cursor) -> None:
        """
        Check_User(connect: Connection, db_create: DB_CREATE,
                cursor: Cursor) -> None
        检查用户表是否存在，不存在则创建

        :param connect: 数据库连接对象
        :param db_create: 数据库创建操作对象
        :param cursor: 光标
        :return: None
        """
        if not self._Check_Table(
                connect=connect,
                cursor=cursor,
                table_name=DB_CONFIG().User,
                table_info=(
                        DB_CONFIG().User_Fields,
                        DB_CONFIG().User_Fields_Types
                )
        ):
            print(f"检测到用户表<{DB_CONFIG().User}>未创建\n"
                  f"自动创建中")
            db_create.User()
            print(f"用户表为<{DB_CONFIG().User}>")

    def Check_Task(self, connect: Connection, db_create: DB_CREATE,
                   cursor: Cursor) -> None:
        """
        Check_Task(connect: Connection, db_create: DB_CREATE,
                cursor: Cursor) -> None
        检查任务表是否存在，不存在则创建

        :param connect: 数据库连接对象
        :param db_create: 数据库创建操作对象
        :param cursor: 光标
        :return: None
        """
        if not self._Check_Table(
                connect=connect,
                cursor=cursor,
                table_name=DB_CONFIG().Task,
                table_info=(
                        DB_CONFIG().Task_Fields,
                        DB_CONFIG().Task_Fields_Types
                )
        ):
            print(f"检测到任务表<{DB_CONFIG().Task}>未创建\n"
                  f"自动创建中")
            db_create.Task()
            print(f"任务表为<{DB_CONFIG().Task}>")

    def Check_Article(self, connect: Connection, db_create: DB_CREATE,
                      cursor: Cursor) -> None:
        """
        Check_Article(connect: Connection, db_create: DB_CREATE,
                    cursor: Cursor) -> None
        检查文章表是否存在，不存在则创建

        :param connect: 数据库连接对象
        :param db_create: 数据库创建操作对象
        :param cursor: 光标
        :return: None
        """
        if not self._Check_Table(
                connect=connect,
                cursor=cursor,
                table_name=DB_CONFIG().Article,
                table_info=(
                        DB_CONFIG().Article_Fields,
                        DB_CONFIG().Article_Fields_Types
                )
        ):
            print(f"检测到文章表<{DB_CONFIG().Article}>未创建\n"
                  f"自动创建中")
            db_create.Article()
            print(f"文章表为<{DB_CONFIG().Article}>")

    def Check_Video(self, connect: Connection, db_create: DB_CREATE,
                    cursor: Cursor) -> None:
        """
        Check_Video(connect: Connection, db_create: DB_CREATE,
                    cursor: Cursor) -> None
        检查视频表是否存在，不存在则创建

        :param connect: 数据库连接对象
        :param db_create: 数据库创建操作对象
        :param cursor: 光标
        :return: None
        """
        if not self._Check_Table(
                connect=connect,
                cursor=cursor,
                table_name=DB_CONFIG().Video,
                table_info=(
                        DB_CONFIG().Video_Fields,
                        DB_CONFIG().Video_Fields_Types
                )
        ):
            print(f"检测到视频表<{DB_CONFIG().Video}>未创建\n"
                  f"自动创建中")
            db_create.Video()
            print(f"视频表为<{DB_CONFIG().Video}>")

    def Check_Table(self, connect: Connection, cursor: Cursor) -> None:
        """
        Check_Table(connect: Connection, cursor: Cursor) -> None
        检查表信息

        :param connect: 数据库连接对象
        :param cursor: 光标
        :return: None
        """
        db_create = DB_CREATE(connect=connect, cursor=cursor)
        self.Check_User(connect=connect, db_create=db_create, cursor=cursor)
        self.Check_Task(connect=connect, db_create=db_create, cursor=cursor)
        self.Check_Article(connect=connect, db_create=db_create, cursor=cursor)
        self.Check_Video(connect=connect, db_create=db_create, cursor=cursor)
