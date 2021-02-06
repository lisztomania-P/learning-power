#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/2/6
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Baidu_AI_Verify.py
# @Function : 验证百度AI
import requests

from inside.DB.Table_Class.Baidu_AI import BAIDU_AI
from inside.Template.Meta_Singleton import SINGLETON
__all__ = ['BAIDU_AI_Verify']


class BAIDU_AI_Verify(metaclass=SINGLETON):
    """百度AI验证类"""

    def Verify(self) -> BAIDU_AI:
        """
        Verify() -> BAIDU_AI
        验证

        Returns: BAIDU_AI

        """
        ak = input("请输入API Key:").strip()
        sk = input("请输入Secret Key:").strip()
        baidu_ai = BAIDU_AI(ak=ak, sk=sk)
        while True:
            temp = self.Check_AS(baidu_ai=baidu_ai)
            if temp == 1:
                break
            elif temp == -1:
                print('API Key错误')
                baidu_ai.Ak = input("请重新输入API Key:").strip()
                continue
            elif temp == -2:
                print('Secret Key错误')
                baidu_ai.Sk = input("请重新输入Secret Key:").strip()
                continue
        return baidu_ai

    @classmethod
    def Check_AS(cls, baidu_ai: BAIDU_AI) -> int:
        """
        Check_AS(baidu_ai: BAIDU_AI) -> int
        检查API Key、Secret Key是否有效

        Args:
            baidu_ai: 百度AI

        Returns:
             1: 有效
            -1: API Key 无效
            -2: Secret Key 无效

        """
        host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type' \
               f'=client_credentials&client_id={baidu_ai.Ak}&client_' \
               f'secret={baidu_ai.Sk}'
        html = requests.get(host)
        if html.json().get('access_token'):
            return 1
        elif html.json().get('error_description') == 'unknown client id':
            return -1
        elif html.json().get('error_description') == 'Client authentication ' \
                                                     'failed':
            return -2
