#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/2/6
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Weekly.py
# @Function :
import base64
import json
import re
from random import randint
from typing import Dict

from inside.Task.Mitmdump.Intercept.ABC_Answer import ABC_ANSWER
__all__ = ['WEEKLY']


class WEEKLY(ABC_ANSWER):
    """每周答题拦截体"""

    def Url_Put(self, url: str) -> bool:
        """
        Url_Put(url: str) -> bool
        提交判断

        :param url: url
        :return: bool
        """
        return "https://pc-proxy-api.xuexi.cn/api/exam/service/practice" \
               "/weekPracticeSubmitV3" == url

    def Url_Res(self, url: str) -> bool:
        """
        Url_Res(url: str) -> bool
        答案判断

        :param url: url
        :return: bool
        """
        res = "https://pc-proxy-api.xuexi.cn/api/exam/service/detail/queryV3" \
              "\\?type=2&id=.*&forced=true"
        if re.match(res, url):
            return True
        return False

    def Extract(self, data: bytes) -> Dict:
        """
        Extract(data: bytes) -> Dict
        提取答案

        :param data: 包含答案的字节数据
        :return: Dict
        """
        data = data.decode('utf-8')
        data = json.loads(data)['data_str']
        return json.loads(base64.b64decode(data).decode('utf-8'))

    def Inject(self, data: bytes, res: Dict) -> bytes:
        """
        Inject(data: bytes, res: Dict) -> bytes
        注入答案

        :param data: 原始提交数据
        :param res: 包含答案数据
        :return: 修改后的提交数据
        """
        data = json.loads(data.decode('utf-8'))
        data['uniqueId'] = res['uniqueId']
        data['questions'].clear()
        data['usedTime'] = randint(20, 50)
        for question in res['questions']:
            data['questions'].append(
                {
                    'questionId': question['questionId'],
                    'answers': question['correct'],
                    'correct': True
                }
            )
        return json.dumps(data).encode('utf-8')
