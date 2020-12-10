#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/2
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : user_msg.py
# @Function : 输出信息共享变量

from typing import Dict
from configuration import TASK_OPTIONS, TASK_ID
USER_MSG: Dict = None
USER_TASKS_NUMBER: Dict = None
USER_ARTICLE_TASKS: int = 0
USER_ARTICLE_PLAYING: int = 0
USER_ARTICLE_TIME: int = 0
USER_VIDEO_TASKS: int = 0
USER_VIDEO_PLAYING: int = 0
USER_VIDEO_TIME: str = ''
USER_DAILY_ANSWER_TASKS: int = 5
USER_DAILY_ANSWER_PLAYING: int = 0
USER_DAILY_ANSWER_TIME_SLEEP: float = 0
USER_WEEKLY_ANSWER_TASKS: int = 5
USER_WEEKLY_ANSWER_PLAYING: int = 0
USER_WEEKLY_ANSWER_TIME_SLEEP: float = 0
USER_PROJECT_ANSWER_TASKS: int = 10
USER_PROJECT_ANSWER_PLAYING: int = 0
USER_PROJECT_ANSWER_TIME_SLEEP: float = 0
