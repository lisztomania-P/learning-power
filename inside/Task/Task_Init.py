#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/24
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Task_Init.py
# @Function : 任务初始化
import base64
import json
from json.decoder import JSONDecodeError
from typing import List

from inside.Config.Api import API
from inside.DB.DB_Manage import DB_MANAGE
from inside.DB.Table_Class.Article import ARTICLE
from inside.DB.Table_Class.Task import TASK
from inside.DB.Table_Class.Video import VIDEO
from inside.Template.Meta_Singleton import SINGLETON
from inside.Tools.Requests import REQUESTS

__all__ = ['TASK_INIT']


class TASK_INIT(metaclass=SINGLETON):
    """任务初始化类"""

    def __init__(self):
        """
        TASK_INIT()
        初始化

        """
        self.__Init_Task()

    @classmethod
    def __Init_Task(cls) -> None:
        """
        任务表初始化(不为空的时候)

        :return: None
        """
        if DB_MANAGE().Task.Empty():
            html = REQUESTS.Get(url=API().Task_Parent.geturl())
            parent = html.json()
            for key in parent.keys():
                son = API().Task_Son.geturl().format(channel_id=key)
                task = TASK(link=son, isread=False)
                DB_MANAGE().Task.Insert(task=task)

    @classmethod
    def Init_Article_Video(cls) -> None:
        """
        Init_Article_Video() -> None
        从任务表中取出任务，进行解析并按类别填入文章表或视频表

        :return: None
        """
        if DB_MANAGE().Task.Exist_Enough():
            task = DB_MANAGE().Task.Query()
            html = REQUESTS.Get(url=task.Link)
            DB_MANAGE().Task.Update(task=task)
            try:
                for temp in html.json():
                    if temp['type'] == 'tuwen':
                        article = ARTICLE(
                            item=temp['itemId'],
                            link=temp['url'],
                            isread=False
                        )
                        DB_MANAGE().Article.Insert(article=article)
                    elif temp['type'] == 'shipin':
                        video = VIDEO(
                            item=temp['itemId'],
                            link=temp['url'],
                            isread=False
                        )
                        DB_MANAGE().Video.Insert(video=video)
            except JSONDecodeError:
                cls.Init_Article_Video()

    def Assigning_Article(self, num: int) -> List[ARTICLE]:
        """
        Assigning_Article(num: int) -> List[ARTICLE]
        获取指定数量的文章任务

        :param num: 任务数
        :return: List[ARTICLE]
        """
        if DB_MANAGE().Article.Exist_Enough(limit=num):
            return DB_MANAGE().Article.Query(limit=num)
        else:
            self.Init_Article_Video()
            return self.Assigning_Article(num=num)

    def Assigning_Video(self, num: int) -> List[VIDEO]:
        """
        Assigning_Video(num: int) -> List[VIDEO]
        获取指定数量的视频任务

        :param num: 任务数
        :return: List[VIDEO]
        """
        if DB_MANAGE().Video.Exist_Enough(limit=num):
            return DB_MANAGE().Video.Query(limit=num)
        else:
            self.Init_Article_Video()
            return self.Assigning_Video(num=num)

    def Assigning_Weekly_Answer(self, token: str) -> int:
        """
        Assigning_Weekly_Answer(token: str) -> int
        获取本周最早且未做的每周答题任务ID

        :param token: 令牌
        :return: int
        """
        cookie = {'token': token}
        html = REQUESTS.Get(
            url=API().Weekly_Answer_Topics.geturl(),
            cookies=cookie
        )
        data = html.json()
        data = json.loads(base64.b64decode(data['data_str']).decode('utf-8'))
        temp = None
        for group in data['list']:
            if group['month'] == '本月':
                temp = group['practices'][::-1]
                break
        for topic in temp:
            if not topic['seeSolution']:
                return topic['id']

    def Assigning_Project_Answer(self, token: str) -> int:
        """
        Assigning_Project_Answer(token: str) -> int
        获取最早且未过期的专项答题任务ID

        :param token: 令牌
        :return: int
        """
        cookie = {'token': token}
        html = REQUESTS.Get(
            url=API().Project_Answer_Topics.geturl(),
            cookies=cookie
        )
        data = html.json()
        data = json.loads(base64.b64decode(data['data_str']).decode('utf-8'))
        for topic in data['list'][::-1]:
            if (not topic['overdue']) and (not topic['seeSolution']):
                return topic['id']