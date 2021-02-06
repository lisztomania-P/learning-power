#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/23
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Options_Manage.py
# @Function : 选项管理
from inside.Config.Path import PATH
from inside.Baidu_AI.Baidu_AI_Manage import BAIDU_AI_MANAGE
from inside.Options.Options import OPTIONS

from inside.Template.Meta_Singleton import SINGLETON
from inside.Tools import Quit

__all__ = ['OPTIONS_MANAGE']


class OPTIONS_MANAGE(metaclass=SINGLETON):
    """选项管理类"""

    @classmethod
    def __Auto(cls) -> None:
        """
        __Auto() -> None
        禁音选项(默认: True)

        :return: None
        """
        auto = input('是否静音(Y/n):').strip()
        if auto in ['y', 'Y', '']:
            OPTIONS().Mute_Audio = True
        else:
            OPTIONS().Mute_Audio = False

    @classmethod
    def __Headless(cls) -> None:
        """
        __Headless() -> None
        显示过程选项(默认: False)

        :return: None
        """
        headless = input('是否显示自动化过程(y/N):').strip()
        if headless in ['y', 'Y']:
            OPTIONS().Headless = False
        else:
            OPTIONS().Headless = True

    @classmethod
    def __Token(cls) -> None:
        """
        __Token() -> None
        持久化选项(默认：True)

        :return: None
        """
        token = input('是否持久化登录(Y/n):').strip()
        if token in ['y', 'Y', '']:
            OPTIONS().Token = True
        else:
            OPTIONS().Token = False

    @classmethod
    def __Baidu_AI(cls) -> None:
        """
        __Baidu_AI() -> None
        百度AI选项(默认：False)

        Returns: None

        """
        baidu_ai = input('是否使用百度AI(y/N):').strip()
        if baidu_ai in ['y', 'Y']:
            OPTIONS().Baidu_AI = True
            BAIDU_AI_MANAGE.Verify()
            with open(PATH().Baidu_AI_On, 'w', encoding='utf-8') as f:
                f.write("1")
                f.close()
        else:
            OPTIONS().Baidu_AI = False
            with open(PATH().Baidu_AI_On, 'w', encoding='utf-8') as f:
                f.write("0")
                f.close()

    @classmethod
    def Init_Options(cls) -> None:
        """
        Options() -> None
        选项初始化

        :return: None
        """
        cls.__Auto()
        cls.__Headless()
        cls.__Token()
        cls.__Baidu_AI()

    @classmethod
    def Task_Options(cls, hint: str = None) -> None:
        """
        Task_Options() -> None
        任务选项初始化

        :return: None
        """
        OPTIONS().Task_Option_Set_Off_All()
        print("可选任务:")
        print("0、全选\t", end='')
        for key, value in OPTIONS().Task_Options.items():
            print(f"{key}、{value}\t", end='')
        print(hint if hint else '')
        options = input("选择任务(空为退出):").strip()
        if not options:
            Quit.Quit()
            exit(code=0)
        try:
            options = set([int(x) for x in options.split()])
            if 0 in options:
                OPTIONS().Task_Option_Set_On_All()
                return None
            if options - set(OPTIONS().Task_Options.keys()):
                cls.Task_Options(hint="\n请输入规定的选项序号")
            for seq in options:
                OPTIONS().Task_Option_Set_On(seq=seq)
        except ValueError:
            cls.Task_Options(hint="\n请输入数字")


_inst = OPTIONS_MANAGE
Init_Options = _inst.Init_Options
