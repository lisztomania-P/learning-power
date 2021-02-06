#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/26
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Intercept11.py
# @Function : 答题拦截注入脚本
import os
import sys
from json import JSONDecodeError
from typing import Dict

"""此处是因为脚本加载Intercept失败，所做的增加搜索路径"""
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(os.path.abspath(__file__))
                )
            )
        )
    )
)
from inside.Task.Mitmdump.Intercept.ABC_Answer import ABC_ANSWER
from inside.Task.Mitmdump.Intercept.Daily import DAILY
from inside.Task.Mitmdump.Intercept.Project import PROJECT
from inside.Task.Mitmdump.Intercept.Weekly import WEEKLY

from mitmproxy.http import HTTPFlow

gears = (DAILY(), WEEKLY(), PROJECT())
gear: ABC_ANSWER = None
put_data: Dict


def request(up: HTTPFlow) -> None:
    if gear:
        if gear.Url_Put(url=up.request.url):
            print("检测到提交，注入中")
            try:
                up.request.content = gear.Inject(
                    data=up.request.content,
                    res=put_data
                )
                print("注入成功")
            except JSONDecodeError:
                print("检测到本次提交为干扰")


def response(down: HTTPFlow):
    for g in gears:
        if g.Url_Res(url=down.request.url):
            try:
                global put_data, gear
                put_data = g.Extract(data=down.response.content)
                gear = g
                print("抓取答案完成")
            except JSONDecodeError:
                pass
