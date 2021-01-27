#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : DB_Article.py
# @Function : 文章表操作
from sqlite3 import Connection, Cursor
from typing import List

from inside.DB.DB_Config import DB_CONFIG
from inside.DB.Table_Class.Article import ARTICLE
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['DB_ARTICLE']


class DB_ARTICLE(metaclass=SINGLETON):
    """文章表操作类"""

    def __init__(self, connect: Connection, cursor: Cursor):
        """
        初始化

        :param connect: 数据库连接对象
        :param cursor: 数据库光标
        """
        self.__connect = connect
        self.__cursor = cursor
        self.__name = DB_CONFIG().Article
        self.__fields = DB_CONFIG().Article_Fields

    def Insert(self, article: ARTICLE) -> None:
        """
        Insert(article: ARTICLE) -> None
        插入文章，如文章已存在则不进行操作

        :param article: 文章
        :return: None
        """
        if not self.Exist(article=article):
            sql = f'''INSERT INTO
                {self.__name} (
                {self.__fields[1]}, 
                {self.__fields[2]}, 
                {self.__fields[3]}) 
                VALUES (?, ?, ?);'''
            data = (
                article.Item,
                article.Link,
                article.Is_Read_DB
            )
            self.__cursor.execute(sql, data)
            self.__connect.commit()

    def Update(self, article: ARTICLE) -> None:
        """
        Update(article: ARTICLE) -> None
        更新文章为已读，如文章不存在则不进行操作

        :param article: 文章
        :return: None
        """
        if self.Exist(article=article):
            sql = f'''UPDATE {self.__name} 
                SET {self.__fields[3]}=1 
                WHERE {self.__fields[1]}=? 
                AND {self.__fields[2]}=?;'''
            data = (
                article.Item,
                article.Link
            )
            self.__cursor.execute(sql, data)
            self.__connect.commit()

    def Update_All(self) -> None:
        """
        Update_All() -> None
        更新所有文章为未读

        :return: None
        """
        sql = f'''UPDATE {self.__name} 
            SET {self.__fields[3]}=0;'''
        self.__cursor.execute(sql)
        self.__connect.commit()

    def Query(self, limit: int) -> List[ARTICLE]:
        """
        Query(limit: int) -> List[ARTICLE]
        随机获取指定数量的未读文章

        :param limit: 数量
        :return: List[ARTICLE]
        """
        sql = f'''SELECT * FROM {self.__name} 
            WHERE {self.__fields[3]}=0 ORDER BY random() LIMIT ?;'''
        data = (limit, )
        result = self.__cursor.execute(sql, data)
        temp = []
        for value in result:
            article = ARTICLE(
                item=value[1],
                link=value[2],
                isread=value[3]
            )
            temp.append(article)
        return temp

    def Exist_Enough(self, limit: int) -> bool:
        """
        Exist_Enough(limit: int) -> bool
        是否存在指定数量的未读文章

        :param limit: 数量
        :return: bool
        """
        sql = f'''SELECT count() FROM {self.__name} 
            WHERE {self.__fields[3]}=0 LIMIT ?;'''
        data = (limit, )
        result = self.__cursor.execute(sql, data)
        temp = next(result)
        return temp[0] >= limit

    def Exist(self, article: ARTICLE) -> bool:
        """
        Exist(article: ARTICLE) -> bool
        是否存在指定的文章

        :param article: 文章
        :return: bool
        """
        sql = f'''SELECT 1 FROM {self.__name} 
                WHERE {self.__fields[1]}=? 
                AND {self.__fields[2]}=?;'''
        data = (
            article.Item,
            article.Link
        )
        result = self.__cursor.execute(sql, data)
        try:
            next(result)
            return True
        except StopIteration:
            return False
