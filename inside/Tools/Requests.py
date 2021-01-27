#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/21
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Requests.py
# @Function : requests初始化
from typing import Dict

import requests
import urllib3
from requests import Response

from inside.Config.User_Agent import USER_AGENT
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['REQUESTS']


class REQUESTS(metaclass=SINGLETON):
    """requests重写类，拥有统一user-agent"""

    __header = {
            'User-Agent': USER_AGENT().User_Agent
        }
    __proxies = {
        'http': 'http://127.0.0.1:8080',
        'https': 'http://127.0.0.1:8080'
    }
    urllib3.disable_warnings()

    @classmethod
    def __Check_Headers(cls, **kwargs) -> Dict:
        """
        __Check_Headers(**kwargs) -> Dict
        检测headers内容进行更新

        :param kwargs: 关键字参数
        :return: Dict
        """
        if kwargs.get('headers'):
            headers = kwargs.pop('headers')
            cls.__header.update(headers)
        return kwargs

    @classmethod
    def Get(cls, url: str, params=None, **kwargs) -> Response:
        """
        Get(url: str, params=None, **kwargs) -> Response
        Get请求

        :param url: 链接
        :param params: 参数
        :param kwargs: 关键字参数
        :return: Response
        """
        kwargs = cls.__Check_Headers(**kwargs)
        html = requests.get(
            url=url,
            headers=cls.__header,
            proxies=cls.__proxies,
            verify=False,
            params=params,
            **kwargs
        )
        html.encoding = html.apparent_encoding
        return html

    @classmethod
    def Post(cls, url: str, data=None, json=None, **kwargs) -> Response:
        """
        Post(url: str, data=None, json=None, **kwargs) -> Response
        Post请求

        :param url:链接
        :param data: 数据
        :param json: 数据
        :param kwargs: 参数
        :return: Response
        """
        kwargs = cls.__Check_Headers(**kwargs)
        html = requests.post(
            url=url,
            headers=cls.__header,
            proxies=cls.__proxies,
            verify=False,
            data=data,
            json=json, **kwargs
        )
        html.encoding = html.apparent_encoding
        return html
