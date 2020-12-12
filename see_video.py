#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author   : lisztomania
# @Date     : 2020/11/28
# @Software : Pycharm
# @Version  : Python 3.8.2
# @File     : see_video.py
# @Function : 视频学习

import time

from selenium.common.exceptions import ElementNotVisibleException

import check_task
import get_random
import out_msg
from selenium.webdriver.support.expected_conditions import \
    presence_of_element_located

from configuration import VIDEO_PLAY_CLASS_NAME1, \
    VIDEO_PLAY_CLASS_NAME2, VIDEO_PLAY_STATUS_CLASS_NAME, \
    VIDEO_TIME_START_CLASS_NAME, VIDEO_TIME_END_CLASS_NAME, \
    VIDEO_PLAYING_CLASS_NAME, VIDEO_PAUSE_CLASS_NAME, \
    PAGE_ROLL_JS
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By


class See_Video(object):
    __success: bool = False
    __page_roll_js: str = PAGE_ROLL_JS
    __video_time_start_class_name = VIDEO_TIME_START_CLASS_NAME
    __video_time_end_class_name = VIDEO_TIME_END_CLASS_NAME
    __play_class_name1 = VIDEO_PLAY_CLASS_NAME1
    __play_class_name2 = VIDEO_PLAY_CLASS_NAME2
    __play_status_class_name = VIDEO_PLAY_STATUS_CLASS_NAME
    __playing_class_name = VIDEO_PLAYING_CLASS_NAME
    __pause_class_name = VIDEO_PAUSE_CLASS_NAME

    def __init__(self):
        pass

    # 点击播放按钮2
    def __play(self, task_driver: WebDriver):
        js = '''
        var d = document.getElementsByTagName("div");
            for (var i=0;i<d.length;i++){
                if(d[i].className == \'''' + self.__play_class_name2 + '''\'){
                    d[i].click();
                    break;
                }
            }'''
        task_driver.execute_script(script=js)

    # 获取进度
    @out_msg.out_print
    def do(self, task_driver: WebDriver, task_url: str, timeout: str):
        task_driver.get(url=task_url)
        if check_task.check_wrap(task_driver=task_driver):
            return None
        # 捕获元素
        wait: WebDriverWait = WebDriverWait(task_driver, 10)
        # 混淆值
        mix: float = get_random.get_random_float(
            a=0,
            b=10
        )
        js: str = self.__page_roll_js.format(450 + mix)
        # 滑动到指定位置
        task_driver.execute_script(script=js)
        # 定位视频时间开始位置
        video_time_start_Ec: presence_of_element_located = \
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME, self.__video_time_start_class_name
                )
            )
        video_time_start: WebElement = wait.until(video_time_start_Ec)
        # 定位视频时间结束位置
        video_time_end_Ec: presence_of_element_located = \
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME, self.__video_time_end_class_name
                )
            )
        video_time_end: WebElement = wait.until(video_time_end_Ec)
        # 获取结束时间
        end: str = video_time_end.get_attribute(name='innerHTML')
        # 避免获取错误的结束时间
        while end == '00:00':
            end: str = video_time_end.get_attribute(name='innerHTML')
            time.sleep(0.1)
        # 定位视频播放按钮1
        play_Ec: presence_of_element_located = EC.presence_of_element_located(
            (
                By.CLASS_NAME, self.__play_class_name1
            )
        )
        play: WebElement = wait.until(play_Ec)
        # 定位播放状态
        play_status_Ec: presence_of_element_located = \
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME, self.__play_status_class_name
                )
            )
        play_status: WebElement = wait.until(play_status_Ec)
        # 点击播放
        try:
            play.click()
        except ElementNotVisibleException:
            pass
        while True:
            start = video_time_start.get_attribute(name='innerHTML')
            # 使视频一直处于播放状态
            if play_status.get_attribute(
                    name='class') != self.__playing_class_name:
                if start == timeout or start == end:
                    break
                else:
                    self.__play(task_driver=task_driver)
            # 避免视频总时间不够预设时间
            if start == timeout or start == end:
                break
            time.sleep(1)
        self.__success = True

    def is_success(self) -> bool:
        return self.__success
