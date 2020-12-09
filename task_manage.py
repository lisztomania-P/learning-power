#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/11/28
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : task_manage.py
# @Function : 任务管理
import get_random
import user_msg
from typing import Dict, List
from selenium.webdriver.chrome.webdriver import WebDriver
from analysis import Analysis_Msg, Analysis_Task, clear_files, \
    Analysis_Weekly_Answer, Analysis_Project_Answer
from configuration import TASK_ID, USER_KEYS, TASK_OPTIONS, VIDEO_TIME, \
    VIDEO_ACC_TIME, ARTICLE_ACC_TIME, DAILY_ANSWER_ACC_TIME, ARTICLE_TIME, \
    WEEKLY_ANSWER_ACC_TIME, PROJECT_ANSWER_ACC_TIME
from answer import Answer
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

    # 文章视频任务解析分发器
    __analysis_task: Analysis_Task = None
    # 每周答题任务解析分发器
    __weekly_task: Analysis_Weekly_Answer = None
    # 专项答题任务解析分发器
    __project_task: Analysis_Project_Answer = None
    # 任务池
    __tasks: Dict = {
        'article': [],
        'video': []
    }

    def __init__(self, driver: WebDriver):
        self.__driver = driver
        # 初始化信息查询窗口
        self.__windows['score'] = self.__driver.current_window_handle
        self.__refresh_user_msg()
        self.__init_user_tasks()

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
        user_msg.USER_ARTICLE_TASKS = max(
            self.__user_tasks_number[self.__task_id[1]],
            self.__user_tasks_number[self.__task_id[1002]]
        )
        user_msg.USER_VIDEO_TASKS = max(
            self.__user_tasks_number[self.__task_id[2]],
            self.__user_tasks_number[self.__task_id[1003]]
        )
        user_msg.USER_DAILY_ANSWER_TASKS = self.__user_tasks_number[
            self.__task_id[6]
        ]
        user_msg.USER_WEEKLY_ANSWER_TASKS = self.__user_tasks_number[
            self.__task_id[5]
        ]
        user_msg.USER_PROJECT_ANSWER_TASKS = self.__user_tasks_number[
            self.__task_id[4]
        ]

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

    # 初始化文章视频任务分发器
    def __init_article_video_tasks(self):
        self.__change_window_task()
        print("初始化文章/视频任务分发器中，需要等待一点时间！")
        self.__analysis_task = Analysis_Task(task_driver=self.__driver)

    # 初始化每周答题任务分发器
    def __init_weekly_answer_tasks(self):
        self.__change_window_task()
        self.__weekly_task = Analysis_Weekly_Answer(task_driver=self.__driver)

    # 初始化专项答题任务分发器
    def __init_project_answer_tasks(self):
        self.__change_window_task()
        self.__project_task = Analysis_Project_Answer(task_driver=self.__driver)

    # 注入任务池(文章)
    def __load_article_tasks(self):
        number = max(self.__user_tasks_number[self.__task_id[1]],
                     self.__user_tasks_number[self.__task_id[1002]])
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
            task_time = get_random.get_random_int(
                a=ARTICLE_TIME[0],
                b=ARTICLE_TIME[1]
            )
            user_msg.USER_ARTICLE_TIME = task_time
            daily_article.do(
                task_driver=self.__driver,
                task_url=task_url,
                timeout=task_time
            )
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
            sec = get_random.get_random_int(a=0, b=9)
            video_time = VIDEO_TIME.format(sec)
            user_msg.USER_VIDEO_TIME = video_time
            video.do(
                task_driver=self.__driver,
                task_url=task_url,
                timeout=video_time
            )
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

    # 执行任务(每日答题)
    def __do_daily_answer_task(self):
        self.__change_window_task()
        daily_answer = Answer(task_driver=self.__driver, task_type=1)
        daily_answer.do_daily()
        self.__init_user_tasks()
        self.__change_window_task()

    # 检查任务6是否完成
    def __check_daily_answer_bar(self) -> bool:
        self.__init_user_tasks()
        if self.__user_tasks_number[self.__task_id[6]]:
            return False
        else:
            return True

    # 执行任务(每周答题)
    def __do_weekly_answer_task(self):
        self.__change_window_task()
        weekly_answer = Answer(task_driver=self.__driver, task_type=2)
        num = self.__weekly_task.get_topic()
        weekly_answer.do_weekly(num=num)
        self.__init_user_tasks()
        self.__change_window_task()

    # 检查任务5是否完成
    def __check_weekly_answer_bar(self) -> bool:
        self.__init_user_tasks()
        if self.__user_tasks_number[self.__task_id[5]]:
            return False
        else:
            return True

    # 执行任务(专项答题)
    def __do_project_answer_task(self):
        self.__change_window_task()
        project_answer = Answer(task_driver=self.__driver, task_type=3)
        num = self.__project_task.get_topic()
        project_answer.do_project(num=num)
        self.__init_user_tasks()
        self.__change_window_task()

    # 检测任务4是否完成
    def __check_project_answer_bar(self) -> bool:
        self.__init_user_tasks()
        if self.__user_tasks_number[self.__task_id[4]]:
            return False
        else:
            return True

    # 完成文章任务
    def __accomplish_article(self):
        while not self.__check_article_bar():
            if not self.__analysis_task:
                self.__init_article_video_tasks()
            self.__check_article_tasks()
            self.__do_article_task()

    # 完成视频任务
    def __accomplish_video(self):
        while not self.__check_video_bar():
            if not self.__analysis_task:
                self.__init_article_video_tasks()
            self.__check_video_tasks()
            self.__do_video_task()

    # 完成每日答题任务
    def __accomplish_daily_answer(self):
        while not self.__check_daily_answer_bar():
            self.__do_daily_answer_task()

    # 完成每周答题任务
    def __accomplish_weekly_answer(self):
        while not self.__check_weekly_answer_bar():
            if not self.__weekly_task:
                self.__init_weekly_answer_tasks()
            self.__do_weekly_answer_task()

    # 完成专项任务
    def __accomplish_project_answer(self):
        while not self.__check_project_answer_bar():
            if not self.__project_task:
                self.__init_project_answer_tasks()
            self.__do_project_answer_task()

    @clear_files
    def start(self):
        if TASK_OPTIONS[1][1]:
            self.__accomplish_article()
            user_msg.USER_ARTICLE_TIME = ARTICLE_ACC_TIME
        if TASK_OPTIONS[2][1]:
            self.__accomplish_video()
            user_msg.USER_VIDEO_TIME = VIDEO_ACC_TIME
        if TASK_OPTIONS[3][1]:
            self.__accomplish_daily_answer()
            user_msg.USER_DAILY_ANSWER_TIME_SLEEP = DAILY_ANSWER_ACC_TIME
        if TASK_OPTIONS[4][1]:
            self.__accomplish_weekly_answer()
            user_msg.USER_WEEKLY_ANSWER_TIME_SLEEP = WEEKLY_ANSWER_ACC_TIME
        if TASK_OPTIONS[5][1]:
            self.__accomplish_project_answer()
            user_msg.USER_PROJECT_ANSWER_TIME_SLEEP = PROJECT_ANSWER_ACC_TIME
        self.__driver.quit()

    def get_tasks(self) -> Dict:
        return self.__tasks

    def get_tasks_number(self) -> Dict:
        return self.__user_tasks_number
