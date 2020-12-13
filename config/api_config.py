#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/13
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : api_config.py
# @Function : api配置
from typing import Dict

# 登录API
LOGIN_API: str = "https://pc.xuexi.cn/points/login.html?ref=https%3A%2F%2Fwww.xuexi.cn%2F"

# 用户信息API
MSG_APIS: Dict = {
    # 累计积分
    'aggregate_score_api': "https://pc-api.xuexi.cn/open/api/score/get?_t=1606620395029",
    # 每日已获积分
    'daily_score_api': "https://pc-api.xuexi.cn/open/api/score/today/query",
    # 任务进度
    'task_bar_api': "https://pc-api.xuexi.cn/open/api/score/today/queryrate",
    # 等级
    'level_api': "https://pc-api.xuexi.cn/open/api/score/self/get"
}

# 文章、视频任务API
TASK_APIS: Dict = {
    # 所有任务类别
    'task_parent_api': "https://www.xuexi.cn/lgdata/channel-list.json?_st=26777175",
    # 具体类别任务总览
    'task_son_api': "https://www.xuexi.cn/lgdata/{}.json?_st=26777175"
}

# 404api
NOT_FOUND_API: str = 'https://www.xuexi.cn/notFound.html'

# 每日答题api
DAILY_ANSWER_API: str = 'https://pc.xuexi.cn/points/exam-practice.html'
# 每日答题答案api
DAILY_ANSWER_RES_API: str = "https://pc-proxy-api.xuexi.cn/api/exam/service/common/deduplicateRandomSearchV3?limit=5&activityCode=QUIZ_ALL&forced=true"

# 每周答题总览api
WEEKLY_ANSWER_TOPICS_API: str = "https://pc-proxy-api.xuexi.cn/api/exam/service/practice/pc/weekly/more?pageSize=50&pageNo={page}"
# 每周答题api
WEEKLY_ANSWER_TOPIC_API: str = "https://pc.xuexi.cn/points/exam-weekly-detail.html?id={num}"
# 每周答题答案api
WEEKLY_ANSWER_RES_API: str = "https://pc-proxy-api.xuexi.cn/api/exam/service/detail/queryV3?type=2&id={num}&forced=true"

# 专项答题总览api
PROJECT_ANSWER_TOPICS_API: str = "https://pc-proxy-api.xuexi.cn/api/exam/service/paper/pc/list?pageSize=50&pageNo={page}"
# 专项答题api
PROJECT_ANSWER_TOPIC_API: str = "https://pc.xuexi.cn/points/exam-paper-detail.html?id={num}"
# 专项答题答案api
PROJECT_ANSWER_RES_API: str = "https://pc-proxy-api.xuexi.cn/api/exam/service/detail/queryV3?type=1&id={num}&forced=true"
