#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/10
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : db_manage.py
# @Function : 数据库管理

import sqlite3
import glob
from sqlite3 import Connection, Cursor
from typing import Tuple, List
from article import Article
from configuration import DB_FILE_DIR
from video import Video

__connect: Connection
__cursor: Cursor


# 检查是否连接装饰器
def __check_connect(func):
    def wrapper(*args, **kwargs):
        try:
            if __connect and __cursor:
                return func(*args, **kwargs)
        except NameError:
            raise Exception("db not connect")

    return wrapper


# 检查是否存在数据库文件
def __check_db() -> bool:
    if glob.glob(pathname=DB_FILE_DIR):
        return True
    return False


# 创建文章表
def __create_article_table() -> bool:
    db_sql: str = '''CREATE TABLE article
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ITEMID TEXT NOT NULL,
    URL TEXT NOT NULL,
    SEE INTEGER NOT NULL
    );'''
    __cursor.execute(db_sql)
    __connect.commit()
    return True


# 创建视频表
def __create_video_table() -> bool:
    db_sql: str = '''CREATE TABLE video
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ITEMID TEXT NOT NULL,
    URL TEXT NOT NULL,
    SEE INTEGER NOT NULL
    );
    '''
    __cursor.execute(db_sql)
    __connect.commit()
    return True


# 连接数据库（对内）
def __connect_db():
    global __connect
    global __cursor
    try:
        if __connect and __cursor:
            pass
    except NameError:
        __connect = sqlite3.connect(database=DB_FILE_DIR)
        __cursor = __connect.cursor()


# 连接数据库（对外）
def connect_db() -> bool:
    if not __check_db():
        __connect_db()
        __create_article_table()
        __create_video_table()
    else:
        __connect_db()
    return True


# 对象类型检查（文章）
def check_article(article: Article) -> bool:
    if article.__class__ == Article:
        return True
    else:
        return False


# 对象类型检查（视频）
def check_video(video: Video) -> bool:
    if video.__class__ == Video:
        return True
    else:
        return False


# 插入文章记录
def insert_article(article: Article) -> bool:
    if not exist_article(article=article):
        db_sql: str = "INSERT INTO article (ITEMID, URL, SEE) " \
                      "VALUES (?, ?, ?);"
        data: Tuple = (
            article.itemId,
            article.url,
            1 if article.see else 0
        )
        __cursor.execute(db_sql, data)
        __connect.commit()
        return True
    else:
        return False


# 删除文章记录
def delete_article(article: Article) -> bool:
    db_sql: str = "DELETE FROM article where ITEMID=? AND URL=?;"
    data: Tuple = (
        article.itemId,
        article.url
    )
    __cursor.execute(db_sql, data)
    __connect.commit()
    return True


# 更新文章记录(内容)
def update_article_msg_id(iid: int, article: Article) -> bool:
    db_sql: str = "UPDATE article set ITEMID=?, URL=?, SEE=? WHERE ID=?;"
    data: Tuple = (
        article.itemId,
        article.url,
        1 if article.see else 0,
        iid
    )
    __cursor.execute(db_sql, data)
    __connect.commit()
    return True


# 更新文章记录（已读）
def update_article_see(article: Article) -> bool:
    db_sql: str = "UPDATE article set SEE=1 WHERE ID=? AND ITEMID=? AND URL=?;"
    data: Tuple = (
        article.id,
        article.itemId,
        article.url
    )
    __cursor.execute(db_sql, data)
    __connect.commit()
    return True


# 提取文章记录
def get_article(limit: int = 1) -> List[Article]:
    db_sql = "SELECT * FROM article WHERE SEE=0 LIMIT ?;"
    data = (limit,)
    result = __cursor.execute(db_sql, data)
    res = [0, []]
    for temp in result:
        article = Article(
            itemId=temp[1],
            url=temp[2],
            see=True if temp[3] else False)
        article.id = temp[0]
        res[1].append(article)
        res[0] += 1
    return res[1] if res[0] == limit else []


# 检查是否存在未读视频记录
def exist_unseen_article(limit: int = 1) -> bool:
    res = get_article(limit=limit)
    return True if res else False


# 查询是否存在文章记录
def exist_article(article: Article) -> bool:
    db_sql: str = "SELECT 1 FROM article WHERE ITEMID=? AND URL=?;"
    data: Tuple = (
        article.itemId,
        article.url
    )
    result = __cursor.execute(db_sql, data)
    try:
        next(result)
        return True
    except StopIteration:
        return False


# 查询是否存在，如不存在就插入
def exist_insert_article(article: Article) -> bool:
    if not exist_article(article=article):
        insert_article(article=article)
        return True
    else:
        return False


# 插入视频记录
def insert_video(video: Video) -> bool:
    if not exist_video(video=video):
        db_sql = "INSERT INTO video (ITEMID, URL, SEE) " \
                 "VALUES (?, ?, ?);"
        data: Tuple = (
            video.itemId,
            video.url,
            1 if video.see else 0
        )
        __cursor.execute(db_sql, data)
        __connect.commit()
        return True
    else:
        return False


# 删除视频记录
def delete_video(video: Video) -> bool:
    db_sql: str = "DELETE FROM video where ITEMID=? AND URL=?;"
    data: Tuple = (
        video.itemId,
        video.url
    )
    __cursor.execute(db_sql, data)
    __connect.commit()
    return True


# 更新视频记录(视频内容)
def update_video_msg_id(iid: int, video: Video) -> bool:
    db_sql: str = "UPDATE video set ITEMID=?, URL=?, SEE=? WHERE ID=?;"
    data: Tuple = (
        video.itemId,
        video.url,
        1 if video.see else 0,
        iid
    )
    __cursor.execute(db_sql, data)
    __connect.commit()
    return True


# 更新视频记录（已读）
def update_video_see(video: Video) -> bool:
    db_sql: str = "UPDATE video set SEE=1 WHERE ID=? AND ITEMID=? AND URL=?;"
    data: Tuple = (
        video.id,
        video.itemId,
        video.url
    )
    __cursor.execute(db_sql, data)
    __connect.commit()
    return True


# 提取视频记录
def get_video(limit: int = 1) -> List[Video]:
    db_sql = "SELECT * FROM video WHERE SEE=0 LIMIT ?;"
    data = (limit,)
    result = __cursor.execute(db_sql, data)
    res = [0, []]
    for temp in result:
        video = Video(
            itemId=temp[1],
            url=temp[2],
            see=True if temp[3] else False
        )
        video.id = temp[0]
        res[1].append(video)
        res[0] += 1
    return res[1] if res[0] == limit else []


# 检查是否存在未读视频记录
def exist_unseen_video(limit: int = 1) -> bool:
    res = get_video(limit=limit)
    return True if res else False


# 查询是否存在视频记录
def exist_video(video: Video) -> bool:
    db_sql: str = "SELECT 1 FROM video WHERE ITEMID=? AND URL=?;"
    data: Tuple = (
        video.itemId,
        video.url
    )
    result = __cursor.execute(db_sql, data)
    try:
        next(result)
        return True
    except StopIteration:
        return False


# 查询是否存在文章，如不存在就插入
def exist_insert_video(video: Video) -> bool:
    if not exist_video(video=video):
        insert_video(video=video)
        return True
    else:
        return False


# 关闭连接
@__check_connect
def close_db() -> bool:
    __connect.close()
    return True
