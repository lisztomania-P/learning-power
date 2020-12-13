#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/11/28
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : login.py
# @Function : 登录

import time
from typing import List

from selenium.common.exceptions import StaleElementReferenceException, \
    InvalidSessionIdException, NoSuchWindowException

from tools.Thread import THREAD
from selenium import webdriver
from selenium.webdriver.support.expected_conditions import \
    presence_of_element_located
from config.path_config import DRIVER_FILE
from config.api_config import LOGIN_API
from config.task_config import QR_CODE_CLASS_NAME, QR_CODE_STATUS_CLASS_NAME, \
    QR_CODE_REFRESH_CLASS_NAME, QR_CODE_LOSE_IDE, QR_CODE_IFRAME_ID, \
    QR_CODE_JS, PAGE_CLEAR_JS

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


class Login(object):
    # 成功标识
    __success: bool = False
    __driver: WebDriver = None
    __wait: WebDriverWait = None

    # 登录页面
    __login_url: str = LOGIN_API
    __qr_iframe: WebElement = None
    __qr_iframe_id: str = QR_CODE_IFRAME_ID
    # 二维码图片(Base64)
    __qr: str = None
    # 二维码
    __qr_code_class_name: str = QR_CODE_CLASS_NAME
    # 二维码状态
    __qr_code_status_class_name: str = QR_CODE_STATUS_CLASS_NAME
    # 二维码失效标识
    __qr_code_lose_ide: str = QR_CODE_LOSE_IDE
    # 二维码刷新
    __qr_code_refresh_class_name: str = QR_CODE_REFRESH_CLASS_NAME
    # 二维码容器
    __qr_vessel: WebDriver = None
    # 二维码线程
    __qr_thread: THREAD = None

    # 图片标签
    __img: WebElement = None
    # 图片状态标签
    __img_status: WebElement = None
    # 图片刷新标签
    __img_refresh: WebElement = None

    # 登录成功的cookies
    __cookies: List = None

    def __init__(self, driver: WebDriver):
        self.__driver = driver
        self.__wait = WebDriverWait(self.__driver, 10)

    # 登录
    def login(self) -> bool:
        # 如已登录成功了，就直接返回成功标志
        if not self.__success:
            self.__driver.get(self.__login_url)
            self.__init_iframe()
            # 切换至二维码页面
            self.__driver.switch_to.frame(frame_reference=self.__qr_iframe)
            self.__init_QR_code()
            self.__manage_QR(on_off=True)
            while True:
                try:
                    temp_cookies = self.__driver.get_cookies()
                except NoSuchWindowException:
                    continue
                # 如果登录成功了，cookies会有'.xuexi.cn'
                temp_cookie = [cookie for cookie in temp_cookies if
                               cookie['domain'] != '.xuexi.cn']
                if not temp_cookie:
                    self.__manage_QR(on_off=False)
                    self.__cookies = temp_cookies
                    self.__success = True
                    # 切回主页面
                    self.__driver.switch_to.default_content()
                    break
        return self.__success

    # 初始化捕获二维码页面
    def __init_iframe(self):
        iframe_Ec: presence_of_element_located = EC.presence_of_element_located \
            (
                (
                    By.ID, self.__qr_iframe_id
                )
            )
        self.__qr_iframe = self.__wait.until(iframe_Ec)

    # 初始化二维码相关标签
    def __init_QR_code(self):
        qr_code_Ec: presence_of_element_located = \
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME, self.__qr_code_class_name
                )
            )
        qr_code: WebElement = self.__wait.until(qr_code_Ec)
        self.__img = qr_code.find_element_by_tag_name(name='img')
        qr_code_status_Ec: presence_of_element_located = \
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME, self.__qr_code_status_class_name
                )
            )
        self.__img_status: WebElement = self.__wait.until(qr_code_status_Ec)
        qr_code_refresh_Ec: presence_of_element_located = \
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME, self.__qr_code_refresh_class_name
                )
            )
        self.__img_refresh: WebElement = self.__wait.until(qr_code_refresh_Ec)

    # 获取二维码图片(Base64)
    def __get_QR_image(self):
        try:
            qr = self.__img.get_attribute(name='src')
            while qr == self.__qr:
                qr = self.__img.get_attribute(name='src')
            self.__qr = qr
        except StaleElementReferenceException:
            pass

    # 检查二维码状态
    def __check_QR_image(self):
        try:
            if self.__img_status.text == self.__qr_code_lose_ide:
                return False
            else:
                return True
        except StaleElementReferenceException:
            pass

    # 刷新二维码
    def __refresh_QR_image(self) -> bool:
        try:
            if self.__img_refresh.is_displayed():
                self.__img_refresh.click()
                return True
            else:
                return False
        except StaleElementReferenceException:
            pass

    # 维持二维码有效
    def __hold_QR_image(self):
        if not self.__check_QR_image():
            self.__refresh_QR_image()
            self.__get_QR_image()
            self.__QR_show()
        time.sleep(0.1)

    # 输出二维码
    def __QR_show(self):
        try:
            js = PAGE_CLEAR_JS + "\n"
            js += QR_CODE_JS.format(self.__qr)
            self.__qr_vessel.execute_script(js)
        except InvalidSessionIdException:
            pass

    # 管理二维码容器
    def __manage_QR(self, on_off: bool = None):
        if on_off and not self.__qr_vessel:
            self.__qr_vessel = webdriver.Chrome(
                executable_path=DRIVER_FILE)
            self.__qr_vessel.set_window_size(width=50, height=350)
            self.__get_QR_image()
            self.__QR_show()
            self.__qr_thread = THREAD(target=self.__hold_QR_image)
            self.__qr_thread.start()
        elif not on_off and self.__qr_vessel:
            self.__qr_thread.stop()
            self.__qr_vessel.quit()

    # 返回cookies
    def get_cookies(self) -> List:
        return self.__cookies
