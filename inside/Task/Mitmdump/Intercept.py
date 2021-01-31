#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/26
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Intercept.py
# @Function : 答题拦截注入脚本
import re
import base64
import json
from json import JSONDecodeError
from random import randint
from typing import Dict, List
from abc import ABCMeta, abstractmethod

from mitmproxy.http import HTTPFlow

__all__ = []


class SINGLETON_ABC(ABCMeta):
    """抽象类的单例元类"""
    __instances = {}

    def __call__(cls, *args, **kwargs):
        """
        重载()，确保返回的为唯一对象

        :param args:
        :param kwargs:
        :return:
        """
        if not cls.__instances.get(cls):
            cls.__instances[cls] = super(SINGLETON_ABC, cls).__call__(*args,
                                                                      **kwargs)
        return cls.__instances[cls]


class ABC_ANSWER(metaclass=SINGLETON_ABC):

    @abstractmethod
    def Url_Put(self, url: str) -> bool:
        pass

    @abstractmethod
    def Url_Res(self, url: str) -> bool:
        pass

    @abstractmethod
    def Extract(self, data: bytes) -> Dict:
        pass

    @abstractmethod
    def Inject(self, data: bytes, res: Dict) -> bytes:
        pass


class DAILY(ABC_ANSWER):

    def Url_Put(self, url: str) -> bool:
        """
        Url_Put(url: str) -> bool
        提交判断

        :param url: url
        :return: bool
        """
        return "https://pc-proxy-api.xuexi.cn/api/exam/service/practice" \
               "/quizSubmitV3" == url

    def Url_Res(self, url: str) -> bool:
        """
        Url_Res(url: str) -> bool
        答案判断

        :param url: url
        :return: bool
        """
        return "https://pc-proxy-api.xuexi.cn/api/exam/service/common" \
               "/deduplicateRandomSearchV3?limit=5&activityCode=QUIZ_ALL" \
               "&forced=true" == url

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


class Weekly(ABC_ANSWER):
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


class Project(ABC_ANSWER):
    """专项答题拦截体"""

    def Url_Put(self, url: str) -> bool:
        """
        Url_Put(url: str) -> bool
        提交判断

        :param url: url
        :return: bool
        """
        return "https://pc-proxy-api.xuexi.cn/api/exam/service/detail/submitV3" \
               == url

    def Url_Res(self, url: str) -> bool:
        """
        Url_Res(url: str) -> bool
        答案判断

        :param url: url
        :return: bool
        """
        res = "https://pc-proxy-api.xuexi.cn/api/exam/service/detail" \
              "/queryV3\\?type=1&id=.*&forced=true"
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

    def __Answer(self, res: Dict) -> List[Dict]:
        """
        __Answer(res: Dict) -> List[Dict]
        由于专项答题没有答案，判题是在云端，所以需要分析答案

        :param res: 包含提示的题目
        :return: List[Dict]
        """
        res_type = res['questionDisplay']
        temp = []
        options = re.findall(r"<font color=\"red\">.*?</font>",
                             res['questionDesc'])
        for index, value in enumerate(options):
            options[index] = value.split('>')[1].split('<')[0]
        if res_type in (1, 2):
            for option in options:
                for answer in res['answers']:
                    if option in answer['content'] or answer['content'] in option:
                        tp = {
                            'answerId': answer['answerId'],
                            'value': answer['label']
                        }
                        if tp not in temp:
                            temp.append(tp)
            if not temp:
                for answer in res['answers']:
                    if answer['content'] in res['questionDesc']:
                        tp = {
                            'answerId': answer['answerId'],
                            'value': answer['label']
                        }
                        if tp not in temp:
                            temp.append(tp)
        elif res_type == 4:
            tp = ''
            for option in options:
                tp += option
            temp.append(
                {
                    'answerId': res['answers'][0]['answerId'],
                    'value': tp
                })
        return temp

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
                    'answers': self.__Answer(res=question)
                }
            )
        return json.dumps(data).encode('utf-8')


gears = (DAILY(), Weekly(), Project())
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
                print(up.request.content)
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
                print(put_data)
                print("抓取答案完成")
            except JSONDecodeError:
                pass
