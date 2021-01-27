#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/20
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Check_Token.py
# @Function : 检测令牌
from inside.Config.Api import API
from inside.Template.Meta_Singleton import SINGLETON

from inside.Tools.Random import RANDOM
from inside.Tools.Requests import REQUESTS

__all__ = ['CHECK_TOKEN']


class CHECK_TOKEN(metaclass=SINGLETON):
    """检查令牌类"""

    @classmethod
    def Check_Token(cls, token: str) -> bool:
        """
        Check_Token(token: str) -> bool
        检查令牌是否有效

        :param token: 令牌
        :return: bool
        """
        cookie = {'token': token}
        link = API().Token_Check.geturl().format(
            timestamp=RANDOM().Float_Precision(a=0, b=1, precision=16)
        )
        html = REQUESTS.Get(
            url=link,
            cookies=cookie
        )
        if html.cookies.get(name='token'):
            return True
        return False
