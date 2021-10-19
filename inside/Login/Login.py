#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/15
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Login.py
# @Function : 登录
import json
import re
from typing import Dict
from urllib import parse

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from inside.Config.Api import API
from inside.Options.Options import OPTIONS
from inside.DB.DB_Manage import DB_MANAGE
from inside.DB.Table_Class.User import USER
from inside.Info.Info_Manage import INFO_MANAGE
from inside.Login.Check_Token import CHECK_TOKEN
from inside.Login.QR_Vessel import QR_VESSEL

from inside.Tools.Network import NETWORK
from inside.Tools.Requests import REQUESTS

__all__ = ['LOGIN']


class LOGIN(object):
    """登录类"""

    def __init__(self, task_driver: WebDriver):
        """
        LOGIN()
        初始化，

        """
        self.__driver = task_driver
        self.__network = NETWORK()
        self.__wait = WebDriverWait(self.__driver, 10)

    def __QR_Iframe(self) -> WebElement:
        """
        __QR_Iframe() -> WebElement
        获取二维码iframe

        :return: WebElement
        """
        iframe_Ec = EC.presence_of_element_located(
            (
                By.ID, "ddlogin-iframe"
            )
        )
        return self.__wait.until(iframe_Ec)

    def __QR_Base64(self) -> str:
        """
        __QR_Base64() -> str
        二维码base64，格式为：data:image/png;base64,xxx==

        :return: str
        """
        qr_code_Ec = EC.presence_of_element_located(
            (By.CLASS_NAME, "login_qrcode_content")
        )
        qr_code: WebElement = self.__wait.until(qr_code_Ec)
        qr = qr_code.find_element_by_tag_name(name='img')
        return qr.get_attribute(name='src')

    def __Get_QR(self) -> str:
        """
        __Get_QR() -> str
        获取二维码，格式为：data:image/png;base64,xxx==

        :return: str
        """
        qr_iframe = self.__QR_Iframe()
        self.__driver.switch_to.frame(frame_reference=qr_iframe)
        temp = self.__QR_Base64()
        self.__driver.switch_to.default_content()
        return temp

    def __Get_QR_ID(self, key: str, value: str) -> str:
        """
        __Get_QR_ID(key: str, value: str) -> str
        获取二维码ID，格式为：qr:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

        :param key: url
        :param value: requestId
        :return: str
        """
        if API().Login_Generate.geturl() == key:
            response = self.__network.GetResponseBody(requestId=value)[
                'body']
            response = json.loads(response)
            return response['result']
        return ''

    def __Get_QR_Status_Network(self, key: str, value: str) -> int:
        """
        __Get_QR_Status_Network(key: str, value: str) -> int
        获取二维码状态码(Network中获取)

        :param key: url
        :param value: requestId
        :return: int
            -1: 还未请求
            1: 成功
            11021: 未登录
            11019: 二维码失效
        """
        if API().Login_QR_Status.geturl() == key:
            while True:
                try:
                    response = self.__network.GetResponseBody(requestId=value)
                    response = json.loads(response['body'])
                    if response['success']:
                        return 1
                    else:
                        return int(response['code'])
                except WebDriverException:
                    continue
        return -1

    def __Get_QR_Status_Requests(self, qr_data: Dict, qr_state: str):
        """
        __Get_QR_Status_Requests(qr_data: Dict) -> int
        获取二维码状态码(requests请求)

        :param qr_data: 带有二维码编号的data
        :param qr_state: 二维码的state
        :return: int
            1: 成功
            11021: 未登录
            11019: 二维码失效
        """
        html = REQUESTS.Post(
            url=API().Login_QR_Status.geturl(),
            data=qr_data
        )
        status = html.json()
        if status['success']:
            self.__Change_Driver_Cookie(key=status['data'], state=qr_state)
            return 1
        else:
            return int(status['code'])

    def __Change_Driver_Cookie(self, key: str, state: str) -> None:
        """
        __Change_Driver_Cookie(key: str, state: str) -> None
        此处是应对network中还未查询二维码状态时，所做的措施，用处是加快登录过程，而不需要浏览器
            自主添加cookie

        :param key: 最后一次查询二维码状态的api会返回code(只会允许查询一次，随后就是过期)
        :param state: iframe链接中提取
        :return: None
        """
        url = parse.urlparse(url=key)
        code = parse.parse_qs(qs=url.query)['loginTmpCode'][0]
        html = REQUESTS.Get(
            url=API().Login_Token.geturl().format(code=code, state=state)
        )
        token = html.cookies.get(name='token')
        cookie = {'domain': '.xuexi.cn',
                  'name': 'token',
                  'value': token}
        self.__driver.add_cookie(cookie_dict=cookie)
        self.__driver.refresh()

    def __Get_QR_State(self, key: str) -> str:
        """
        __Get_QR_State(key: str) -> str
        获取二维码的state，在iframe链接中提取

        :param key: iframe链接
        :return: str
        """
        temp = re.match(
            pattern=API().Login_QR_Iframe.geturl(),
            string=key
        )
        if temp:
            url = parse.urlparse(url=key)
            return parse.parse_qs(qs=url.query)['state'][0]
        return ''

    def __QR_Refresh(self) -> None:
        """
        __QR_Refresh() -> None
        刷新二维码

        :return: None
        """
        qr_refresh_Ec = EC.presence_of_element_located(
            (
                By.CLASS_NAME, "refresh"
            )
        )
        qr_refresh: WebElement = self.__wait.until(qr_refresh_Ec)
        qr_refresh.click()

    def __Check_Status(self) -> bool:
        """
        __Check_Status() -> bool
        检测二维码状态， 此处略微复杂了一点
        具体流程：
            1、初始化state、iid、status、req为空
                state：二维码的state值，用于处理浏览器未触发状态检测的空窗期登录问题
                iid：二维码的id值，作用同上
                status：二维码的状态值
                req：检测浏览器是否处于空窗期
            2、开启循环
            3、从日志中取值
            4、为state、iid、status、req赋值
            5、如果日志中没有了、且初值都赋值完毕，且浏览器处于空窗期，就进行自主查询
            6、判断查询的状态

        :return: bool
            True：成功
            False：过期
        """
        state = iid = status = None
        req = False
        while True:
            network = self.__network.Get()
            for key, value in network.items():
                key = parse.unquote(string=key)
                temp = self.__Get_QR_State(key=key)
                if temp:
                    state = temp
                    break
                temp = self.__Get_QR_ID(key=key, value=value)
                if temp:
                    iid = temp
                    break
                status = self.__Get_QR_Status_Network(key=key, value=value)
                if status == 11019:
                    return False
                req = True if status == -1 else False
            if not network and state and iid and status and req:
                qr_data = {
                    'qrCode': iid,
                    'goto': 'https://www.xuexi.cn',
                    'pdmToken': ''
                }
                status = self.__Get_QR_Status_Requests(
                    qr_data=qr_data,
                    qr_state=state
                )
            if status == 1:
                return True
            elif status == 11021:
                continue

    def _Login(self) -> bool:
        """
        _Login() -> Bool
        进行登录；
        具体流程：
            1、开启循环检测二维码状态
                1、获取二维码图片
                2、显示二维码
                3、二维码状态检测
                4、根据3的返回值决定：
                    1、刷新二维码，中断本次循环，再来一次
                    2、提取Token值，根据选项(持久化)决定是否保持token，关闭二维码容器
        :return: Bool，返回值只有True，如未登录则会一直循环
        """
        self.__network.Clear()
        self.__driver.get(url=API().Login.geturl())
        while True:
            qr = self.__Get_QR()
            QR_VESSEL().Show_QR(qr=qr)
            status = self.__Check_Status()
            if not status:
                self.__QR_Refresh()
                continue
            else:
                while self.__driver.current_url != API().Master.geturl():
                    continue
                cookies = self.__driver.get_cookies()
                token = [{cookie['name']: cookie['value']} for cookie in
                         cookies if cookie['name'] == 'token']
                if token:
                    INFO_MANAGE().Init(token=token[0]['token'])
                    if OPTIONS().Token:
                        cookie = token[0]
                        html = REQUESTS().Get(
                            url=API().Aggregate_Score.geturl(),
                            cookies=cookie
                        )
                        data = html.json()
                        user_id = data['data']['userId']
                        user = USER(user_id=user_id, token=token[0]['token'])
                        if DB_MANAGE().User.Exist_User(user=user):
                            DB_MANAGE().User.Update(user=user)
                        else:
                            DB_MANAGE().User.Insert(user=user)
                            DB_MANAGE().Article.Update_All()
                            DB_MANAGE().Video.Update_All()
                QR_VESSEL().QR_QUIT()
                return status

    def Login(self) -> bool:
        """
        Login() -> bool
        登录，如果user表不为空会检测令牌是否有效，有效则直接登录

        :return: bool
        """
        if DB_MANAGE().User.Exist():
            user = DB_MANAGE().User.Query()
            if CHECK_TOKEN.Check_Token(token=user.Token):
                INFO_MANAGE().Init(token=user.Token)
                self.__driver.get(url=API().Master.geturl())
                self.__driver.add_cookie(cookie_dict=user.Token_Driver)
                self.__driver.refresh()
                return True
        return self._Login()

