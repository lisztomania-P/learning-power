#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2021/1/25
# @Software : Pycharm
# @Version  : Python 3.8.5
# @File     : Task_Answer.py
# @Function : 答题任务
import re
import time

from tqdm import tqdm
from typing import List

from selenium.common.exceptions import StaleElementReferenceException, \
    ElementClickInterceptedException, TimeoutException, \
    NoAlertPresentException, NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver

from inside.Config.Api import API
from inside.Template.Meta_Singleton import SINGLETON
from inside.Template.Task_Exception import TASK_EXCEPTION
from inside.Tools.Network import NETWORK

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By

__all__ = ['TASK_ANSWER']


class TASK_ANSWER(metaclass=SINGLETON):
    """答题任务类"""

    def __init__(self, driver: WebDriver):
        """
        TASK_ANSWER(driver: WebDriver)
        初始化

        :param driver: 驱动
        """
        self.__driver = driver
        self.__network = NETWORK()
        self.__wait = WebDriverWait(self.__driver, 10)

    def Topic_Type(self) -> str:
        """
        Topic_Type() -> str
        题目类型

        :return: str
        """
        topic_type_ec = EC.presence_of_element_located(
            (
                By.CLASS_NAME, 'q-header'
            )
        )
        topic_type: WebElement = self.__wait.until(topic_type_ec)
        return topic_type.text.strip()

    def Topic_Seq(self) -> str:
        """
        Topic_Seq() -> str
        题目序号，返回'x/x'

        :return: str
        """
        topic_seq_ec = EC.presence_of_element_located(
            (
                By.CLASS_NAME, 'pager'
            )
        )
        topic_seq: WebElement = self.__wait.until(topic_seq_ec)
        return topic_seq.text.strip()

    def Topic_Input(self) -> List[WebElement]:
        """
        Topic_Input() -> WebElement
        填空题输入框

        :return: WebElement
        """
        topic_input_ec = EC.presence_of_all_elements_located(
            (
                By.TAG_NAME, 'input'
            )
        )
        return self.__wait.until(topic_input_ec)

    def Topic_Options(self) -> List[WebElement]:
        """
        Topic_Options() -> List[WebElement]
        选择题选项

        :return: List[WebElement]
        """
        topic_options_ec = EC.presence_of_element_located(
            (
                By.CLASS_NAME, 'q-answers'
            )
        )
        topic_options: WebElement = self.__wait.until(topic_options_ec)
        return topic_options.find_elements_by_tag_name(name='div')

    def Topic_Submit(self) -> WebElement:
        """
        Topic_Submit() -> WebElement
        题目提交按钮

        :return: WebElement
        """
        topic_submits_ec = EC.presence_of_element_located(
            (
                By.CLASS_NAME, 'action-row'
            )
        )
        topic_submits: WebElement = self.__wait.until(topic_submits_ec)
        submits = topic_submits.find_elements_by_tag_name(name='button')
        for submit in submits:
            if submit.is_enabled():
                return submit

    def __Accomplish(self) -> bool:
        """
        __Accomplish() -> bool
        检测答题是否完成

        :return: bool
        """
        while True:
            for key, value in self.__network.Get().items():
                if re.match(
                    pattern=API().Answer_Accomplish.geturl(),
                    string=key
                ):
                    return True

    def __Error(self) -> bool:
        """
        __Error() -> bool
        检测是否有弹窗

        :return: bool
        """
        try:
            time.sleep(1)
            self.__driver.find_element_by_class_name(
                name='ant-modal-content')
            return True
        except NoSuchElementException:
            return False

    def __Alert(self) -> None:
        """
        __Alert() -> None
        检测弹窗，并点击确认

        :return: None
        """
        try:
            self.__driver.switch_to.alert.accept()
        except NoAlertPresentException:
            pass

    def __Do(self) -> None:
        """
        __Do() -> None
        做一个题目

        :return: None
        """
        topic_type = self.Topic_Type()
        print(topic_type)
        if '填空题' in topic_type:
            for answer in self.Topic_Input():
                answer.send_keys('1')
        elif [x for x in ('单选题', '多选题') if x in topic_type]:
            for answer in self.Topic_Options():
                answer.click()
        time.sleep(0.1)
        topic_seq = self.Topic_Seq()
        while self.Topic_Seq() == topic_seq:
            topic_submit = self.Topic_Submit()
            topic_submit.click()
            if self.__Error():
                raise TASK_EXCEPTION('失败')

    def Do(self, link: str) -> None:
        """
        Do(link: str) -> None
        答题

        :param link: 题目链接
        :return: None
        """
        self.__network.Clear()
        self.__driver.get(url=link)
        self.__Alert()
        seq = int(self.Topic_Seq().split('/')[-1])
        bar = tqdm(
            desc='答题',
            total=seq,
            unit='题',
            leave=False,
            ncols=70
        )
        while True:
            try:
                self.__Do()
                bar.update(n=1)
            except (StaleElementReferenceException,
                    ElementClickInterceptedException,
                    TimeoutException):
                self.__Accomplish()
                bar.update(n=1)
                time.sleep(0.1)
                break
        bar.close()
