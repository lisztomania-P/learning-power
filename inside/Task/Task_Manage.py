#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/25
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Task_Manage.py
# @Function : 任务管理器
import time

from tqdm import tqdm
from selenium.webdriver.chrome.webdriver import WebDriver

from inside.Config.Api import API
from inside.DB.DB_Manage import DB_MANAGE
from inside.DB.Table_Class.Project import PROJECT
from inside.Info.Info_Manage import INFO_MANAGE
from inside.Options.Options import OPTIONS
from inside.Task.Task_Answer import TASK_ANSWER
from inside.Task.Task_Article_Video import TASK_ARTICLE_VIDEO
from inside.Task.Task_Init import TASK_INIT
from inside.Template.Meta_Singleton import SINGLETON
from inside.Template.Task_Exception import TASK_EXCEPTION
from inside.Tools.Output import OUTPUT

__all__ = ['TASK_MANAGE']


class TASK_MANAGE(metaclass=SINGLETON):
    """任务管理类"""

    def __init__(self, driver: WebDriver):
        """
        TASK_MANAGE(driver: WebDriver)
        初始化

        :param driver: 驱动
        """
        self.__driver = driver
        self.__answer_time = (time.time(), False)

    def __Article(self, num: int, tq: int) -> None:
        """
        __Article(num: int) -> None
        进行文章任务

        :param num: 任务数量
        :return: None
        """
        temp = TASK_ARTICLE_VIDEO(task_driver=self.__driver)
        tasks = TASK_INIT().Assigning_Article(num=num)
        bar = tqdm(
            desc='文章',
            total=num,
            unit='it',
            leave=False,
            ncols=70
        )
        for task in tasks:
            temp.Do(task=task, tq=tq)
            DB_MANAGE().Article.Update(article=task)
            bar.update(n=1)
            OUTPUT.Info()
        bar.close()

    def __Video(self, num: int, tq: int) -> None:
        """
        __Video(num: int) -> None
        进行视频任务

        :param num: 任务数量
        :return: None
        """
        temp = TASK_ARTICLE_VIDEO(task_driver=self.__driver)
        tasks = TASK_INIT().Assigning_Video(num=num)
        bar = tqdm(
            desc='视频',
            total=num,
            unit='it',
            leave=False,
            ncols=70
        )
        for task in tasks:
            temp.Do(task=task, tq=tq)
            DB_MANAGE().Video.Update(video=task)
            bar.update(n=1)
            OUTPUT.Info()
        bar.close()

    def __Check_Article(self) -> None:
        """
        __Check_Article() -> None
        监测文章任务的完成

        :return: None
        """
        while True:
            bar = INFO_MANAGE().Task_Bar
            if bar['193549965443299840'].Current_Score != bar['193549965443299840'].Day_Max_Score:
                p = bar['193549965443299840'].Day_Max_Score - bar['193549965443299840'].Current_Score
                self.__Article(num=p, tq=5)
            else:
                break

    def __Check_Video(self) -> None:
        """
        __Check_Video() -> None
        监测视频任务的完成

        :return: None
        """
        while True:
            bar = INFO_MANAGE().Task_Bar
            p = bar['193551054368504064'].Day_Max_Score - bar['193551054368504064'].Current_Score
            c = bar['193551711926319360'].Day_Max_Score - bar['193551711926319360'].Current_Score
            if p and not c:
                self.__Video(num=p, tq=1)
            elif p and c:
                self.__Video(num=p, tq=(c*4)//p)
            elif not p and c:
                self.__Video(num=1, tq=c*4)
            else:
                break

    def __Check_Daily_Answer(self) -> None:
        """
        __Check_Daily_Answer() -> None
        监测每日答题任务的完成

        :return: None
        """
        while True:
            bar = INFO_MANAGE().Task_Bar
            if bar['193552647163836928'].Current_Score != bar['193552647163836928'].Day_Max_Score:
                if self.__answer_time[-1]:
                    if time.time() - self.__answer_time[0] <= 10:
                        continue
                temp = TASK_ANSWER(driver=self.__driver)
                temp.Do(link=API().Daily_Answer.geturl())
                OUTPUT.Info()
                self.__answer_time = (time.time(), True)
            else:
                break

    def __Check_Weekly_Answer(self) -> None:
        """
        __Check_Weekly_Answer() -> None
        监测每周答题任务的完成

        :return: None
        """
        while True:
            bar = INFO_MANAGE().Task_Bar
            if bar['193554171675900416'].Current_Score != bar['193554171675900416'].Day_Max_Score:
                if self.__answer_time[-1]:
                    if time.time() - self.__answer_time[0] <= 10:
                        continue
                token = self.__driver.get_cookie(name='token')['value']
                iid = TASK_INIT().Assigning_Weekly_Answer(token=token)
                if not iid:
                    print("没有每周答题任务了")
                    break
                temp = TASK_ANSWER(driver=self.__driver)
                temp.Do(link=API().Weekly_Answer_Topic.geturl().format(num=iid))
                OUTPUT.Info()
                self.__answer_time = (time.time(), True)
            else:
                break

    def __Check_Project_Answer(self) -> None:
        """
        __Check_Project_Answer() -> None
        监测专项答题任务的完成

        :return: None
        """
        while True:
            bar = INFO_MANAGE().Task_Bar
            if bar['193561952390838784'].Current_Score != bar['193561952390838784'].Day_Max_Score:
                if self.__answer_time[-1]:
                    if time.time() - self.__answer_time[0] <= 10:
                        continue
                token = self.__driver.get_cookie(name='token')['value']
                iid = TASK_INIT().Assigning_Project_Answer(token=token)
                if not iid:
                    print("没有专项答题任务了")
                    break
                temp = TASK_ANSWER(driver=self.__driver)
                try:
                    temp.Do(link=API().Project_Answer_Topic.geturl().format(num=iid))
                except TASK_EXCEPTION:
                    DB_MANAGE().Project.Insert(PROJECT(pid=iid))
                OUTPUT.Info()
                self.__answer_time = (time.time(), True)
            else:
                break

    def Task(self) -> None:
        """
        Task() -> None
        根据选项执行相应的任务

        :return: None
        """
        if OPTIONS().Article:
            self.__Check_Article()
        if OPTIONS().Video:
            self.__Check_Video()
        if OPTIONS().Daily_Answer:
            self.__Check_Daily_Answer()
        if OPTIONS().Weekly_Answer:
            self.__Check_Weekly_Answer()
        if OPTIONS().Project_Answer:
            self.__Check_Project_Answer()
