#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : DB_Video.py
# @Function : 视频表操作
from sqlite3 import Connection, Cursor
from typing import List

from inside.DB.DB_Config import DB_CONFIG
from inside.DB.Table_Class.Video import VIDEO
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['DB_VIDEO']


class DB_VIDEO(metaclass=SINGLETON):
    """视频表操作类"""

    def __init__(self, connect: Connection, cursor: Cursor):
        """
        初始化

        :param connect: 数据库连接对象
        :param cursor: 数据库光标
        """
        self.__connect = connect
        self.__cursor = cursor
        self.__name = DB_CONFIG().Video
        self.__fields = DB_CONFIG().Video_Fields

    def Insert(self, video: VIDEO) -> None:
        """
        Insert(video: VIDEO) -> None
        插入视频，如视频已存在则不进行操作

        :param video: 视频
        :return: None
        """
        if not self.Exist(video=video):
            sql = f'''INSERT INTO
                {self.__name} 
                ({self.__fields[1]}, 
                {self.__fields[2]}, 
                {self.__fields[3]})
                VALUES (?, ?, ?);'''
            data = (
                video.Item,
                video.Link,
                video.Is_Read_DB
            )
            self.__cursor.execute(sql, data)
            self.__connect.commit()

    def Update(self, video: VIDEO) -> None:
        """
        Update(video: VIDEO) -> None
        更新视频为已读，如视频不存在则不进行操作

        :param video: 视频
        :return: None
        """
        if self.Exist(video=video):
            sql = f'''UPDATE {self.__name} 
                SET {self.__fields[3]}=1 
                WHERE {self.__fields[1]}=? 
                AND {self.__fields[2]}=?;'''
            data = (
                video.Item,
                video.Link
            )
            self.__cursor.execute(sql, data)
            self.__connect.commit()

    def Update_All(self) -> None:
        """
        Update_All() -> None
        更新所有视频为未读

        :return: None
        """
        sql = f'''UPDATE {self.__name} 
            SET {self.__fields[3]}=0;'''
        self.__cursor.execute(sql)
        self.__connect.commit()

    def Query(self, limit: int) -> List[VIDEO]:
        """
        Query(limit: int) -> List[VIDEO]
        随机获取指定数量的未读视频

        :param limit: 数量
        :return: List[VIDEO]
        """
        sql = f'''SELECT * FROM {self.__name} 
            WHERE {self.__fields[3]}=0 ORDER BY RANDOM() LIMIT ?;'''
        data = (limit, )
        result = self.__cursor.execute(sql, data)
        temp = []
        for value in result:
            video = VIDEO(
                item=value[1],
                link=value[2],
                isread=value[3]
            )
            temp.append(video)
        return temp

    def Exist_Enough(self, limit: int) -> bool:
        """
        Exist_Enough(limit: int) -> bool
        是否存在指定数量的未读视频

        :param limit: 数量
        :return: bool
        """
        sql = f'''SELECT count() FROM {self.__name} 
            WHERE {self.__fields[3]}=0 LIMIT ?;'''
        data = (limit, )
        result = self.__cursor.execute(sql, data)
        temp = next(result)
        return temp[0] >= limit

    def Exist(self, video: VIDEO) -> bool:
        """
        Exist(video: VIDEO) -> bool
        是否存在指定的视频

        :param video: 视频
        :return: bool
        """
        sql = f'''SELECT 1 FROM {self.__name} 
            WHERE {self.__fields[1]}=? 
            AND {self.__fields[2]}=?;'''
        data = (
            video.Item,
            video.Link
        )
        result = self.__cursor.execute(sql, data)
        try:
            next(result)
            return True
        except StopIteration:
            return False
