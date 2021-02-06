#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/2/6
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Baidu_AI_Manage.py
# @Function : 百度AI管理类
from inside.Baidu_AI.Baidu_AI_Verify import BAIDU_AI_Verify
from inside.Baidu_AI.Baidu_AI_Tools import BAIDU_AI_TOOLS
from inside.Template.Meta_Singleton import SINGLETON
from inside.DB.DB_Manage import DB_MANAGE
__all__ = ['BAIDU_AI_MANAGE']


class BAIDU_AI_MANAGE(metaclass=SINGLETON):
    """百度AI管理类"""

    @classmethod
    def Verify(cls) -> None:
        """
        Verify() -> None
        验证百度AI

        Returns: None

        """
        baidu_ai = None
        if not DB_MANAGE().Baidu_AI.Empty():
            baidu_ai = DB_MANAGE().Baidu_AI.Query()
            if BAIDU_AI_Verify.Check_AS(baidu_ai=baidu_ai) != 1:
                baidu_ai = None
        if not baidu_ai:
            baidu_ai = BAIDU_AI_Verify().Verify()
            DB_MANAGE().Baidu_AI.Insert(baidu_ai=baidu_ai)

    @classmethod
    def Tools(cls) -> BAIDU_AI_TOOLS:
        """
        Tools() -> BAIDU_AI_TOOLS
        返回百度AI工具

        Returns: BAIDU_AI_TOOLS

        """
        baidu_ai = DB_MANAGE().Baidu_AI.Query()
        return BAIDU_AI_TOOLS(baidu_ai=baidu_ai)
