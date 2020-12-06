#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/11/28
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : task_manage.py
# @Function : 任务管理

import user_msg
from typing import Dict, List
from selenium.webdriver.chrome.webdriver import WebDriver
from analysis import Analysis_Msg, Analysis_Task, clear_files
from configuration import TASK_ID, USER_KEYS, TASK_OPTIONS
from daily_article import Daily_Article
from video import Video


class Task_Manage(object):
    # 任务总状态
    __accomplish: bool = False
    # 任务ID
    __task_id: Dict = TASK_ID
    # 窗口管理
    __windows: Dict = dict()
    # 用户信息
    __user_msg: Dict = dict()
    # 用户信息键
    __user_keys: Dict = USER_KEYS
    # 待完成任务数
    __user_tasks_number: Dict = dict()

    # 任务解析分发器
    __analysis_task: Analysis_Task = None
    # 任务池
    __tasks: Dict = {
        'article': [],
        'video': []
    }

    def __init__(self, driver: WebDriver):
        self.__driver = driver
        # 初始化信息查询窗口
        self.__windows['score'] = self.__driver.current_window_handle
        self.__init_user_tasks()
        self.__init_tasks()

    # 刷新用户信息
    def __refresh_user_msg(self):
        self.__change_window_score()
        analysis_msg = Analysis_Msg(score_driver=self.__driver)
        self.__user_msg[self.__user_keys[1]] = analysis_msg.get_uid()
        self.__user_msg[
            self.__user_keys[2]] = analysis_msg.get_aggregate_score()
        self.__user_msg[self.__user_keys[3]] = analysis_msg.get_daily_score()
        self.__user_msg[self.__user_keys[4]] = analysis_msg.get_task_bar()
        self.__user_msg[self.__user_keys[5]] = analysis_msg.get_level()
        user_msg.USER_MSG = self.__user_msg

    # 初始化任务数
    def __init_user_tasks(self):
        self.__refresh_user_msg()
        task_bar = self.__user_msg[self.__user_keys[4]]
        for task_id, task_name in self.__task_id.items():
            task: Dict = task_bar[self.__task_id[task_id]]
            task_number = task['dayMaxScore'] - task['currentScore']
            self.__user_tasks_number[self.__task_id[task_id]] = task_number
        user_msg.USER_TASKS_NUMBER = self.__user_tasks_number

    # 创建积分获取窗口
    def __create_score_window(self):
        score_window: str = self.__windows.get('score')
        if score_window is None or \
                score_window not in self.__driver.window_handles:
            self.__driver.execute_script("window.open();")
            temp_handles: List[str] = self.__driver.window_handles
            task_window: str = self.__windows.get('task')
            if task_window in temp_handles:
                temp_handles.remove(task_window)
            self.__windows['score'] = temp_handles[0]

    # 创建任务窗口
    def __create_task_window(self):
        task_window: str = self.__windows.get('task')
        if task_window is None or \
                task_window not in self.__driver.window_handles:
            self.__driver.execute_script("window.open();")
            temp_handles: List[str] = self.__driver.window_handles
            score_window: str = self.__windows.get('score')
            if score_window in temp_handles:
                temp_handles.remove(score_window)
            self.__windows['task'] = temp_handles[0]

    # 更改为积分窗口
    def __change_window_score(self):
        score_window = self.__windows.get('score')
        if score_window is None:
            self.__create_score_window()
        self.__driver.switch_to.window(self.__windows.get('score'))

    # 更改为任务窗口
    def __change_window_task(self):
        task_window = self.__windows.get('task')
        if task_window is None:
            self.__create_task_window()
        self.__driver.switch_to.window(self.__windows.get('task'))

    # 初始化任务分发器
    def __init_tasks(self):
        self.__change_window_task()
        self.__analysis_task = Analysis_Task(task_driver=self.__driver)

    # 注入任务池(文章)
    def __load_article_tasks(self):
        number = max(self.__user_tasks_number[self.__task_id[1]],
                     self.__user_tasks_number[self.__task_id[1002]])
        user_msg.USER_ARTICLE_TASKS = number
        self.__tasks['article'] = self.__analysis_task.get_article_tasks(
            task_number=number)

    # 检查任务池(文章)
    def __check_article_tasks(self):
        if not self.__tasks['article']:
            self.__load_article_tasks()

    # 注入任务池(视频)
    def __load_video_tasks(self):
        number = max(self.__user_tasks_number[self.__task_id[2]],
                     self.__user_tasks_number[self.__task_id[1003]])
        user_msg.USER_VIDEO_TASKS = number
        self.__tasks['video'] = self.__analysis_task.get_video_tasks(
            task_number=number)

    # 检查任务池(视频)
    def __check_video_tasks(self):
        if not self.__tasks['video']:
            self.__load_video_tasks()

    # 执行任务(文章)
    def __do_article_task(self):
        self.__change_window_task()
        for task in self.__tasks['article']:
            user_msg.USER_ARTICLE_PLAYING = \
                self.__tasks['article'].index(task) + 1
            daily_article = Daily_Article()
            task_url = task[1]['url']
            daily_article.do(task_driver=self.__driver, task_url=task_url)
            self.__analysis_task.update_parend_son(task=task)
            self.__init_user_tasks()
            self.__change_window_task()
        self.__tasks['article'].clear()

    # 检查任务1、1002任务是否完成
    def __check_article_bar(self) -> bool:
        self.__init_user_tasks()
        if self.__user_tasks_number[self.__task_id[1]] or \
                self.__user_tasks_number[self.__task_id[1002]]:
            return False
        else:
            return True

    # 执行任务(视频)
    def __do_video_task(self):
        self.__change_window_task()
        for task in self.__tasks['video']:
            user_msg.USER_VIDEO_PLAYING = self.__tasks['video'].index(task) + 1
            video = Video()
            task_url = task[1]['url']
            video.do(task_driver=self.__driver, task_url=task_url)
            self.__analysis_task.update_parend_son(task=task)
            self.__init_user_tasks()
            self.__change_window_task()
        self.__tasks['video'].clear()

    # 检查任务2、1003是否完成
    def __check_video_bar(self) -> bool:
        self.__init_user_tasks()
        if self.__user_tasks_number[self.__task_id[2]] or \
                self.__user_tasks_number[self.__task_id[1003]]:
            return False
        else:
            return True

    # 完成文章任务
    def __accomplish_article(self):
        while not self.__check_article_bar():
            self.__check_article_tasks()
            self.__do_article_task()

    # 完成视频任务
    def __accomplish_video(self):
        while not self.__check_video_bar():
            self.__check_video_tasks()
            self.__do_video_task()

    @clear_files
    def start(self):
        if TASK_OPTIONS[1][1]:
            self.__accomplish_article()
            print("文章任务完成")
        if TASK_OPTIONS[2][1]:
            self.__accomplish_video()
            print("视频任务完成")
        self.__driver.quit()

    def get_tasks(self) -> Dict:
        return self.__tasks

    def get_tasks_number(self) -> Dict:
        return self.__user_tasks_number
