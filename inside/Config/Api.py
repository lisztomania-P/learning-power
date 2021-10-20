#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/12/13
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : Api.py
# @Function : api配置
from typing import List
from urllib.parse import ParseResult
from urllib.parse import urlparse

from inside.Driver.Driver_Analysis import GOOGLEAPIS_DRIVER_ANALYSIS, \
    TAOBAO_DRIVER_ANALYSIS
from inside.Template.ABC_Driver_Analysis import DRIVER_ANALYSIS
from inside.Template.Meta_Singleton import SINGLETON

__all__ = ['API']

from inside.Tools.Url_Test import URL_TEST


class API(metaclass=SINGLETON):
    """Api集合类"""

    @property
    def Master(self) -> ParseResult:
        """
        Master -> ParseResult
        官网

        :return: ParseResult
        """
        return urlparse(
            url="https://www.xuexi.cn/"
        )

    @property
    def Login(self) -> ParseResult:
        """
        Login -> ParseResult
        登录api

        :return: ParseResult
        """
        return urlparse(
            url="https://pc.xuexi.cn/points/login.html?ref=https://www.xuexi"
                ".cn/"
        )

    @property
    def Login_Generate(self) -> ParseResult:
        """
        Login_Generate -> ParseResult
        登录二维码号码api

        :return: ParseResult
        """
        return urlparse(
            url="https://login.xuexi.cn/user/qrcode/generate"
        )

    @property
    def Login_QR_Status(self) -> ParseResult:
        """
        Login_State -> ParseResult
        登录二维码状态api

        :return: ParseResult
        """
        return urlparse(
            url="https://login.xuexi.cn/login/login_with_qr"
        )

    @property
    def Login_QR_Iframe(self) -> ParseResult:
        """
        Login_QR_Iframe -> ParseResult
        登录二维码state的正则规则api

        :return: ParseResult
        """
        return urlparse(
            url="https://login.xuexi.cn/login/xuexiWeb\\?appid"
                "=dingoankubyrfkttorhpou&goto=https://oa.xuexi.cn&type=1"
                "&state=.*?&check_login=https://pc-api.xuexi.cn"
        )

    @property
    def Login_Token(self) -> ParseResult:
        """
        Login_Token -> ParseResult
        登录cookie获取api

        :return: ParseResult
        """
        return urlparse(
            url="https://pc-api.xuexi.cn/login/secure_check?code={"
                "code}&state={state}"
        )

    @property
    def Token_Check(self) -> ParseResult:
        """
        Token_Check(self) -> ParseResult
        Token检测api

        :return: ParseResult
        """
        return urlparse(
            url="https://pc-api.xuexi.cn/open/api/auth/check?t={timestamp}"
        )

    @property
    def Aggregate_Score(self) -> ParseResult:
        """
        Aggregate_Score -> ParseResult
        总积分api

        :return: ParseResult
        """
        return urlparse(
            url="https://pc-api.xuexi.cn/open/api/score/get?_t=1606620395029"
        )

    @property
    def Daily_Score(self) -> ParseResult:
        """
        Daily_Score -> ParseResult
        每日已获积分api

        :return: ParseResult
        """
        return urlparse(
            url="https://pc-api.xuexi.cn/open/api/score/today/query"
        )

    @property
    def Task_Bar(self) -> ParseResult:
        """
        Task_Bar -> ParseResult
        每日任务进度api

        :return: ParseResult
        """
        return urlparse(
            url="https://pc-proxy-api.xuexi.cn/api/score/days/listScoreProgress?sence=score&deviceType=2"
        )

    @property
    def Level(self) -> ParseResult:
        """
        Level -> ParseResult
        等级api

        :return: ParseResult
        """
        return urlparse(
            url="https://pc-api.xuexi.cn/open/api/score/self/get"
        )

    @property
    def Task_Parent(self) -> ParseResult:
        """
        Task_Parent -> ParseResult
        所有任务类别api

        :return: ParseResult
        """
        return urlparse(
            url="https://www.xuexi.cn/lgdata/channel-list.json?_st=26777175"
        )

    @property
    def Task_Son(self) -> ParseResult:
        """
        Task_Son -> ParseResult
        具体任务集合api，此处返回Url中需格式化后使用，格式变量为channel_id，此变量值从
            Task_Parent中解析而来;
            使用方法：Task_Son.geturl().format(channel_id=xxx)

        :return: ParseResult
        """
        return urlparse(
            url="https://www.xuexi.cn/lgdata/{channel_id}.json?_st=26777175"
        )

    @property
    def Task_Check(self) -> ParseResult:
        return urlparse(
            url="https://iflow-api.xuexi.cn/logflow/api/v1/pclog"
        )

    @property
    def Not_Found(self) -> ParseResult:
        """
        Not_Found -> ParseResult
        404api

        :return: ParseResult
        """
        return urlparse(
            url="https://www.xuexi.cn/notFound.html"
        )

    @property
    def Daily_Answer(self) -> ParseResult:
        """
        Daily_Answer -> ParseResult
        每日答题api

        :return: ParseResult
        """
        return urlparse(
            url="https://pc.xuexi.cn/points/exam-practice.html"
        )

    @property
    def Daily_Answer_Res(self) -> ParseResult:
        """
        Daily_Answer_Res -> ParseResult
        每日答题答案api

        :return: ParseResult
        """
        return urlparse(
            url="https://pc-proxy-api.xuexi.cn/api/exam/service/common"
                "/deduplicateRandomSearchV3?limit=5&activityCode=QUIZ_ALL"
                "&forced=true"
        )

    @property
    def Daily_Answer_Put(self) -> ParseResult:
        """
        Daily_Answer_Put -> ParseResult
        每日答题答案提交api

        :return: ParseResult
        """
        return urlparse(
            url="https://pc-proxy-api.xuexi.cn/api/exam/service/practice"
                "/quizSubmitV3"
        )

    @property
    def Answer_Accomplish(self) -> ParseResult:
        """
        Answer_Accomplish -> ParseResult
        答题完成api

        :return: ParseResult
        """
        return urlparse(
            url="https://pc-proxy-api.xuexi.cn/api/exam/service/detail/score"
                "\\?queryTipScoreId=.*"
        )

    @property
    def Weekly_Answer_Topics(self) -> ParseResult:
        """
        Weekly_Answer_Topics -> ParseResult
        每周答题总览api，由于每周答题2021/01/10改版，所有答题不过期，所以将获取往期未答；
            而目前总共为3页，所以num从3开始，其实可以调整pageSize的大小，一次性将题目列表
            全部获取，但不是正常的操作。

        :return: ParseResult
        """
        return urlparse(
            url="https://pc-proxy-api.xuexi.cn/api/exam/service/practice/pc"
                "/weekly/more?pageSize=50&pageNo={num}"
        )

    @property
    def Weekly_Answer_Topic(self) -> ParseResult:
        """
        Weekly_Answer_Topic -> ParseResult
        每周答题api，此处返回Url中需格式化后使用，格式变量为num，此变量值从
            Weekly_Answer_Topics中解析而来。
            使用方法：Weekly_Answer_Topic.geturl().format(num=x)

        :return: ParseResult
        """
        return urlparse(
            url="https://pc.xuexi.cn/points/exam-weekly-detail.html?id={num}"
        )

    @property
    def Weekly_Answer_Res(self) -> ParseResult:
        """
        Weekly_Answer_Res -> ParseResult
        每周答题答案api，此处返回Url中需格式化后使用，格式变量为num，此变量值从
            Weekly_Answer_Topics中解析而来并与Weekly_Answer_Topic统一;
            使用方法：Weekly_Answer_Res.geturl().format(num=x)

        :return: ParseResult
        """
        return urlparse(
            url="https://pc-proxy-api.xuexi.cn/api/exam/service/detail"
                "/queryV3?type=2&id={num}&forced=true"
        )

    @property
    def Project_Answer_Topics(self) -> ParseResult:
        """
        Project_Answer_Topics -> ParseResult
        专项答题总览api，由于每周答题2021/01/10改版，所有答题不过期，所以将获取往期未答；
            而目前总共为5页，所以num从5开始，其实可以调整pageSize的大小，一次性将题目列表
            全部获取，但不是正常的操作。

        :return: ParseResult
        """
        return urlparse(
            url="https://pc-proxy-api.xuexi.cn/api/exam/service/paper/pc"
                "/list?pageSize=50&pageNo={num}"
        )

    @property
    def Project_Answer_Topic(self) -> ParseResult:
        """
        Project_Answer_Topic -> ParseResult
        专项答题api，此处返回Url中需格式化后使用，格式变量为page，此变量值从
            Project_Answer_Topics解析而来。
            使用方法：Project_Answer_Topic.geturl().format(num=x)

        :return: ParseResult
        """
        return urlparse(
            url="https://pc.xuexi.cn/points/exam-paper-detail.html?id={num}"
        )

    @property
    def Project_Answer_Res(self) -> ParseResult:
        """
        Project_Answer_Res -> ParseResult
        专项答题答案api，此处返回Url中需格式化后使用，格式变量为num，此变量值从
            Project_Answer_Topics中解析而来并与Project_Answer_Topic统一;
            使用方法：Project_Answer_Res.geturl().format(num=x)

        :return: ParseResult
        """
        return urlparse(
            url="https://pc-proxy-api.xuexi.cn/api/exam/service/detail"
                "/queryV3?type=1&id={num}&forced=true"
        )

    @property
    def __Drivers(self) -> List[DRIVER_ANALYSIS]:
        """
        __Drivers -> List[ParseResult]
        驱动下载站点集合

        :return: List[ParseResult]
        """
        google = GOOGLEAPIS_DRIVER_ANALYSIS()
        taobao = TAOBAO_DRIVER_ANALYSIS()
        return [google, taobao]

    @property
    def Driver(self) -> DRIVER_ANALYSIS:
        """
        Driver -> DRIVER_ANALYSIS
        测试所有驱动下载站点，返回最佳站点

        :return: DRIVER_ANALYSIS
        """
        temp = float('inf')
        driver = None
        for value in self.__Drivers:
            test = URL_TEST.Url_Test(url=value.Master.geturl())
            if test and test < temp:
                temp = test
                driver = value
        return driver
