#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/13
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : can_change_config.py
# @Function : 可更改配置

from typing import Tuple

# 文章页面时长随机（秒）
ARTICLE_TIME: Tuple = (75, 90)

# 视频页面时长随机（秒）
VIDEO_TIME: str = "01:2{}"

# 答题间隔时长随机（秒）
DAILY_ANSWER_TIME_SLEEP: Tuple = (3, 5)

# 进度条长度
BAR_LENGTH: int = 70
