#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/1
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : out_msg.py
# @Function : 输出信息

import os
import user_msg
from configuration import TASK_ID, TASK_IDE, ARTICLE_ACC_TIME, \
    VIDEO_ACC_TIME, DAILY_ANSWER_ACC_TIME


# 输出用户信息
def out_user_msg():
    msg = '''用户ID:{uid}
    段位:{l_name}\t等级:{l_level}
    {a_name}:{a_score}\t{d_name}:{d_score}
    '''
    msg = msg.format(
        uid=user_msg.USER_MSG['uid'],
        l_name=user_msg.USER_MSG['level']['name'],
        l_level=user_msg.USER_MSG['level']['level'],
        a_name=user_msg.USER_MSG['aggregate_score']['name'],
        a_score=user_msg.USER_MSG['aggregate_score']['score'],
        d_name=user_msg.USER_MSG['daily_score']['name'],
        d_score=user_msg.USER_MSG['daily_score']['score']
    )
    print(msg)


# 输出可获分数
def out_tasks_numbers():
    msg = '''剩余可获分数:
    {name_1}:{score_1}\t{name_2}:{score_2}\t{name_4}:{score_4}\t{name_5}:{score_5}\t{name_6}:{score_6}
    {name_7}:{score_7}\t{name_8}:{score_8}\t{name_9}:{score_9}\t{name_10}:{score_10}\t{name_11}:{score_11}
    {name_12}:{score_12}\t{name_13}:{score_13}\t{name_14}:{score_14}\t{name_15}:{score_15}\t{name_1002}:{score_1002}
    {name_1003}:{score_1003}\t{name_1004}:{score_1004}\t{name_2001}:{score_2001}\t{name_2002}:{score_2002}\t{name_2003}:{score_2003}
    {name_10001}:{score_10001}\t{name_10004}:{score_10004}
    '''
    ev = "msg.format("
    for key, value in TASK_ID.items():
        ml = "name_{key}=TASK_IDE['{value}'], score_{" \
             "key}=user_msg.USER_TASKS_NUMBER['{value}'], "
        ml = ml.format(key=key, value=value)
        ev += ml
    ev = ev[:-2] + ")"
    msg = eval(ev)
    print(msg)


# 输出文章任务进度
def out_article_bar():
    msg = '''文章任务:{play}/{max_task}\n'''
    msg = msg.format(
        play=user_msg.USER_ARTICLE_PLAYING,
        max_task=user_msg.USER_ARTICLE_TASKS
    )
    date = '''单个执行时间:{sec}秒'''
    if user_msg.USER_ARTICLE_TIME:
        if user_msg.USER_ARTICLE_TIME == ARTICLE_ACC_TIME:
            date = "文章任务已完成"
        else:
            date = date.format(sec=user_msg.USER_ARTICLE_TIME)
        msg += date
    print(msg)


# 输出视频任务进度
def out_video_bar():
    msg = '''视频任务:{play}/{max_task}\n'''
    msg = msg.format(
        play=user_msg.USER_VIDEO_PLAYING,
        max_task=user_msg.USER_VIDEO_TASKS
    )
    date = '''单个执行时间:{minute}'''
    if user_msg.USER_VIDEO_TIME:
        if user_msg.USER_VIDEO_TIME == VIDEO_ACC_TIME:
            date = "视频任务已完成"
        else:
            date = date.format(minute=user_msg.USER_VIDEO_TIME)
        msg += date
    print(msg)


# 输出每日答题任务进度
def out_daily_answer_bar():
    msg = '''每日答题任务:{play}/{max_task}\n'''
    msg = msg.format(
        play=user_msg.USER_DAILY_ANSWER_PLAYING,
        max_task=user_msg.USER_DAILY_ANSWER_TASKS
    )
    time_msg = '随机等待时间:{time_sleep}秒'
    if user_msg.USER_DAILY_ANSWER_TIME_SLEEP:
        if user_msg.USER_DAILY_ANSWER_TIME_SLEEP == DAILY_ANSWER_ACC_TIME:
            print("每日答题任务已完成")
        else:
            time_msg = time_msg.format(
                time_sleep=user_msg.USER_DAILY_ANSWER_TIME_SLEEP
            )
        msg += time_msg
    print(msg)


# 输出装饰器
def out_print(func):
    def wrapper(*args, **kwargs):
        os.system('cls')
        try:
            out_user_msg()
            out_tasks_numbers()
            if user_msg.TASK_OPTIONS[1][1]:
                out_article_bar()
            if user_msg.TASK_OPTIONS[2][1]:
                out_video_bar()
            if user_msg.TASK_OPTIONS[3][1]:
                out_daily_answer_bar()
        except:
            pass
        return func(*args, **kwargs)

    return wrapper
