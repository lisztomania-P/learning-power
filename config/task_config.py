#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/13
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : task_config.py
# @Function : 任务配置

from typing import Dict

# 任务ID
TASK_ID: Dict = {
    # 阅读文章
    1: 'read_article',
    # 视听学习
    2: 'video',
    # 专项答题
    4: 'project_answer',
    # 每周答题
    5: 'weekly_answer',
    # 每日答题
    6: 'daily_answer',
    # 分享
    7: 'share',
    # 收藏
    8: 'collect',
    # 登录
    9: 'login',
    # 订阅
    10: 'subscription',
    # 发表观点
    11: 'viewpoint',
    # 挑战答题
    12: 'challenge_answer',
    # 参加调查问卷活动
    13: 'questionnaire',
    # 本地频道
    14: 'local_channel',
    # 强国运动
    15: 'exercise',
    # 文章时长
    1002: 'article_time',
    # 视听学习时长
    1003: 'video_time',
    # 连续学习达标
    1004: 'continuous',
    # 积分补发
    2001: 'supply_again',
    # 积分优化
    2002: 'optimize',
    # 违规扣减
    2003: 'violation',
    # 争上游答题
    10001: 'most_answer',
    # 双人对战
    10004: 'double_against'
}

# 任务说明
TASK_IDE: Dict = {
    'read_article': '阅读文章',
    'video': '视听学习',
    'project_answer': '专项答题',
    'weekly_answer': '每周答题',
    'daily_answer': '每日答题',
    'share': '分享',
    'collect': '收藏',
    'login': '登录',
    'subscription': '订阅',
    'viewpoint': '发表观点',
    'challenge_answer': '挑战答题',
    'questionnaire': '参加调查问卷活动',
    'local_channel': '本地频道',
    'exercise': '强国运动',
    'article_time': '文章时长',
    'video_time': '视听学习时长',
    'continuous': '连续学习达标',
    'supply_again': '积分补发',
    'optimize': '积分优化',
    'violation': '违规扣减',
    'most_answer': '争上游答题',
    'double_against': '双人对战',
}

# 用户信息键
USER_KEYS: Dict = {
    # 用户ID
    1: 'uid',
    # 累计积分
    2: 'aggregate_score',
    # 每日积分
    3: 'daily_score',
    # 任务进度
    4: 'task_bar',
    # 等级
    5: 'level'
}

# 二维码容器添加二维码
QR_CODE_JS: str = '''
        var img = document.createElement("img");
        img.src="{}";
        document.body.appendChild(img);
'''
# 清空页面
PAGE_CLEAR_JS: str = "document.body.innerHTML='';"
# 页面滚动
PAGE_ROLL_JS: str = "document.documentElement.scrollTop={}"


# 登录页面
# 二维码iframe
QR_CODE_IFRAME_ID: str = "ddlogin-iframe"
# 二维码
QR_CODE_CLASS_NAME: str = "login_qrcode_content"
# 状态
QR_CODE_STATUS_CLASS_NAME: str = "login_qrcode_text"
QR_CODE_LOSE_IDE: str = "二维码失效，点击刷新"
# 刷新
QR_CODE_REFRESH_CLASS_NAME: str = "login_qrcode_refresh"

# 维护页面
WRAP_CLASS_NAME: str = "text-wrap"

# 文章任务完成标志
ARTICLE_ACC_TIME = -1

# 视频任务完成标志
VIDEO_ACC_TIME: str = "--:--"
# 视频当前时间标签
VIDEO_TIME_START_CLASS_NAME: str = "current-time"
# 视频结束时间标签
VIDEO_TIME_END_CLASS_NAME: str = "duration"
# 视频播放按钮标签
VIDEO_PLAY_CLASS_NAME1: str = "outter"
# 视频播放按钮标签
VIDEO_PLAY_CLASS_NAME2: str = "prism-play-btn"
# 视频播放状态标签
VIDEO_PLAY_STATUS_CLASS_NAME: str = "prism-big-play-btn"
# 视频正在播放标识
VIDEO_PLAYING_CLASS_NAME: str = "prism-big-play-btn playing"
# 视频暂停标识
VIDEO_PAUSE_CLASS_NAME: str = "prism-big-play-btn pause"

# 每日答题任务完成标志
DAILY_ANSWER_ACC_TIME: float = -1.0
# 每周答题任务完成标志
WEEKLY_ANSWER_ACC_TIME: float = -1.0
# 专项答题任务完成标志
PROJECT_ANSWER_ACC_TIME: float = -1.0
# 题目
DAILY_ANSWER_TOPIC_CLASS_NAME: str = 'q-body'
# 选择选项
DAILY_ANSWER_CHOOSABLE_CLASS_NAME: str = 'q-answers'
# 选择列表
DAILY_ANSWER_CHOOSABLE_TAG_NAME: str = 'div'
# 提交按钮容器
DAILY_ANSWER_SUBMIT_CLASS_NAME: str = 'action-row'
# 提交按钮
DAILY_ANSWER_SUBMIT_TAG_NAME: str = 'button'

# 任务选项
TASK_OPTIONS: Dict = {
    1: ['文章', False],
    2: ['视频', False],
    3: ['每日答题', False],
    4: ['每周答题', False],
    5: ['专项答题（此项有点BUG）', False]
}