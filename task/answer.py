#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/11/28
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : answer.py
# @Function : 答题任务
import base64
import re
import time
import json
from json.decoder import JSONDecodeError
from typing import List, Dict, Tuple
from selenium.common.exceptions import NoAlertPresentException, \
    WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import \
    presence_of_element_located

from tools import get_random
from config import out_msg, user_msg
from config.api_config import DAILY_ANSWER_API, DAILY_ANSWER_RES_API, \
    WEEKLY_ANSWER_TOPIC_API, WEEKLY_ANSWER_RES_API, PROJECT_ANSWER_TOPIC_API, \
    PROJECT_ANSWER_RES_API
from config.task_config import DAILY_ANSWER_SUBMIT_CLASS_NAME, \
    DAILY_ANSWER_SUBMIT_TAG_NAME, DAILY_ANSWER_CHOOSABLE_CLASS_NAME, \
    DAILY_ANSWER_CHOOSABLE_TAG_NAME, DAILY_ANSWER_TOPIC_CLASS_NAME
from config.can_change_config import DAILY_ANSWER_TIME_SLEEP
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


class Answer(object):
    __success: bool = False
    __type: int = 0
    __is_end: bool = False
    __wait: WebDriverWait = None
    __driver: WebDriver = None
    __answer_topic: WebElement = None
    __answer_topic_desc: str = None
    __answer_input: List[WebElement] = None
    __answer_choosables: Dict = None
    __submit_container: WebElement = None
    __answer_submit: WebElement = None

    __topic_class_name: str = DAILY_ANSWER_TOPIC_CLASS_NAME
    __submit_class_name: str = DAILY_ANSWER_SUBMIT_CLASS_NAME
    __choosable_class_name: str = DAILY_ANSWER_CHOOSABLE_CLASS_NAME
    __choosable_tag_name: str = DAILY_ANSWER_CHOOSABLE_TAG_NAME
    __submit_tag_name: str = DAILY_ANSWER_SUBMIT_TAG_NAME
    __time: Tuple = DAILY_ANSWER_TIME_SLEEP

    __answer_list: List[Dict] = None

    def __init__(self, task_driver: WebDriver, task_type: int):
        self.__driver = task_driver
        self.__type = task_type
        self.__wait = WebDriverWait(self.__driver, 10)

    # 初始化题目标签
    def __init_topic(self):
        topic_Ec: presence_of_element_located = EC.presence_of_element_located(
            (
                By.CLASS_NAME, self.__topic_class_name
            )
        )
        self.__answer_topic = self.__wait.until(topic_Ec)
        self.__extract_topic_desc(topic_tag=self.__answer_topic)

    # 解析题目
    def __extract_topic_desc(self, topic_tag: WebElement):
        self.__answer_topic_desc = topic_tag.text.replace('（）', '')

    # 初始化输入框标签
    def __init_input(self):
        self.__answer_input = self.__answer_topic.find_elements_by_tag_name(
            name='input'
        )

    # 初始化选项标签
    def __init_choosable(self):
        choosable_Ec: presence_of_element_located = \
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME, self.__choosable_class_name
                )
            )
        choosables: WebElement = self.__wait.until(choosable_Ec)
        self.__extract_choosables(choosables=choosables)

    # 解析选项
    def __extract_choosables(self, choosables: WebElement):
        answer_choosable = choosables.find_elements_by_tag_name(
            name=self.__choosable_tag_name
        )
        self.__answer_choosables = dict()
        for choosable in answer_choosable:
            self.__answer_choosables[choosable.text.split('. ')[0]] = \
                choosable

    # 初始化按钮容器
    def __init_submits(self):
        submit_Ec: presence_of_element_located = \
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME, self.__submit_class_name
                )
            )
        self.__submit_container: WebElement = self.__wait.until(submit_Ec)

    # 初始化提交按钮
    def __init_submit(self):
        self.__init_submits()
        answer_submits = self.__submit_container.find_elements_by_tag_name(
            name=self.__submit_tag_name
        )
        for submit in answer_submits:
            if submit.text == '交 卷':
                self.__answer_submit = submit
                self.__is_end = True
                break
            self.__answer_submit = submit

    # 解析答案
    def __init_answer(self, url: str):
        time.sleep(3)
        log_performance = self.__driver.get_log(log_type='performance')
        for log in log_performance:
            log['message'] = json.loads(log['message'])
        answer_list = []
        for log in log_performance:
            try:
                if log['message']['message']['params']['request']['url'] == \
                        url:
                    answer_list.append(log)
            except KeyError:
                continue
        for answer in answer_list:
            try:
                requestId = answer['message']['message']['params']['requestId']
                res = self.__driver.execute_cdp_cmd(
                    cmd='Network.getResponseBody',
                    cmd_args={'requestId': requestId}
                )
                res['body'] = json.loads(res['body'])
                result = base64.b64decode(
                    res['body']['data_str']
                ).decode('utf-8')
                result = json.loads(result)
                self.__answer_list = result['questions']
            except (WebDriverException, TypeError, JSONDecodeError):
                continue

    # # 初始化标签
    # def __init_tag(self):
    #     self.__init_topic()
    #     self.__init_submit()

    def __do_choosable(self, answer: Dict):
        self.__init_choosable()
        if self.__type in [1, 2]:
            for correct in answer['correct']:
                self.__answer_choosables[correct['value']].click()
                time.sleep(0.1)
        elif self.__type == 3:
            descs = re.findall(
                pattern=r"<font color=\"red\">.*?</font>",
                string=answer['questionDesc']
            )
            for index, desc in enumerate(descs):
                descs[index] = desc[desc.find('>')+1: desc.rfind('<')]
            for correct in answer['answers']:
                for desc in descs:
                    if correct['content'] == desc:
                        self.__answer_choosables[correct['label']].click()
                        time.sleep(0.1)

    def __do_input(self, answer: Dict):
        self.__init_input()
        if self.__type in [1, 2]:
            for answer_input, correct in zip(
                    self.__answer_input,
                    answer['correct']
            ):
                answer_input.send_keys(correct['value'])
        elif self.__type == 3:
            descs = re.findall(
                pattern=r"<font color=\"red\">.*?</font>",
                string=answer['questionDesc']
            )
            for index, desc in enumerate(descs):
                descs[index] = desc[desc.find('>')+1: desc.rfind('<')]
            for answer_input, desc in zip(
                self.__answer_input,
                descs
            ):
                answer_input.send_keys(desc)

    # 执行一次答题
    @out_msg.out_print
    def __do(self, time_sleep: float):
        time.sleep(time_sleep)
        self.__init_topic()
        for answer in self.__answer_list:
            if self.__answer_topic_desc in answer['body'].replace('（）', ''):
                Type = answer['questionDisplay']
                if Type in [1, 2]:
                    self.__do_choosable(answer=answer)
                    break
                elif Type == 4:
                    self.__do_input(answer=answer)
                    break
        time.sleep(time_sleep)
        self.__init_submit()
        self.__answer_submit.click()

    # 检查弹窗
    def __check_alert(self):
        try:
            self.__driver.switch_to.alert.accept()
        except NoAlertPresentException:
            pass

    # 执行每日答题
    def do_daily(self):
        self.__driver.get(url=DAILY_ANSWER_API)
        self.__check_alert()
        self.__init_answer(url=DAILY_ANSWER_RES_API)
        for num in range(int(user_msg.USER_DAILY_ANSWER_TASKS)):
            user_msg.USER_DAILY_ANSWER_PLAYING += 1
            time_sleep: float = get_random.get_random_float(
                a=self.__time[0],
                b=self.__time[1]
            )
            user_msg.USER_DAILY_ANSWER_TIME_SLEEP = time_sleep * 2
            self.__do(time_sleep=time_sleep)
        user_msg.USER_DAILY_ANSWER_PLAYING = 0
        self.__success = True

    # 执行每周答题
    def do_weekly(self, num: int):
        self.__driver.get(url=WEEKLY_ANSWER_TOPIC_API.format(num=num))
        self.__check_alert()
        self.__init_answer(url=WEEKLY_ANSWER_RES_API.format(num=num))
        for i in range(int(user_msg.USER_WEEKLY_ANSWER_TASKS)):
            user_msg.USER_WEEKLY_ANSWER_PLAYING += 1
            time_sleep: float = get_random.get_random_float(
                a=self.__time[0],
                b=self.__time[1]
            )
            user_msg.USER_WEEKLY_ANSWER_TIME_SLEEP = time_sleep * 2
            self.__do(time_sleep=time_sleep)
            if self.__is_end:
                break
        user_msg.USER_WEEKLY_ANSWER_PLAYING = 0
        self.__success = True

    # 执行专项答题
    def do_project(self, num: int):
        self.__driver.get(url=PROJECT_ANSWER_TOPIC_API.format(num=num))
        self.__check_alert()
        self.__init_answer(url=PROJECT_ANSWER_RES_API.format(num=num))
        for i in range(int(user_msg.USER_PROJECT_ANSWER_TASKS)):
            user_msg.USER_PROJECT_ANSWER_PLAYING += 1
            time_sleep: float = get_random.get_random_float(
                a=self.__time[0],
                b=self.__time[1]
            )
            user_msg.USER_PROJECT_ANSWER_TIME_SLEEP = time_sleep * 2
            self.__do(time_sleep=time_sleep)
        user_msg.USER_PROJECT_ANSWER_PLAYING = 0
        self.__success = True

    def is_success(self) -> bool:
        return self.__success
